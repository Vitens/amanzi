<template>
  <div id="menu">
  <i class="fa fa-cube"></i>
  <menu id="main-menu">
    <li v-for="item, index in menu" :key="index" @click="toggleSubmenu">
      <span  @mouseenter="submenuIndex=index" class="main-item">{{ $t('ui.menubar.' + item.name + '.label') }}</span>
      <Transition name="el-zoom-in-top">
        <ul v-show="submenuIndex == index && submenu">
          <li v-for="subitem, subindex in getItems(item)" :key="subindex" :class="{separator: subitem.separator, disabled: isDisabled(subitem)}" @click.stop="handleAction(subitem)">
            <template v-if="!subitem.separator">
            <span class="checked" v-if="subitem.checked && subitem.checked.bind(this)()">✓</span>
            <template v-if="subitem.notranslate">
              {{ subitem.name }}
            </template>
            <template v-else>
              {{ $t('ui.menubar.' + item.name + '.' + subitem.name) }}
            </template>

            <span class="shortcut" v-if="subitem.shortcut">{{ shortcut(subitem.shortcut) }}</span>
            </template>
          </li>
        </ul>
      </Transition>
    </li>
  </menu>
  <template v-if="$project.unsaved">
    <el-button @click="$project.save()" class="save-button" type="warning" size="small">{{ $t('ui.menubar.unsaved') }} &nbsp;<i class="fa fa-download"></i></el-button>
  </template>
  <template v-if="!$project.unsaved">
    <span class='saved'>{{ $t('ui.menubar.saved') }} </span>
  </template>
  <div class="version">
    v{{ $version }}
  </div>
  </div>


</template>
<script>
import { ElMessageBox } from 'element-plus'

let menu = [
  {
    name: 'project',
    items: [
      { name: 'new', shortcut: 'mod+N', action: function() {this.requestNew() } },
      { name: 'open', shortcut: 'mod+O', action: function() {this.upload()} },
      { name: 'save', shortcut: 'mod+S',
        action: function() {this.$project.save()}
       },
      { name: 'download', action: function() { this.download() } },
      { separator: true },
      { name: 'rename', action: function() { this.rename() } },
      { separator: true },
      { name: 'keyfigures', action: function() {this.$project.edit_key_figures() } },
      { name: 'report', action: function() { this.$project.run_report() } }
    ]
    },
    {
    name: 'edit',
    items: [
      { name: 'undo', shortcut: 'mod+Z', 
      disabled: function() {return this.$project.undoStack.length == 0}, 
      action: function() {this.$project.$undo()} 
      },
      { name: 'redo', shortcut: 'mod+Y',
      disabled: function() {return this.$project.redoStack.length == 0},
      action: function() {this.$project.$redo()}
      },
      { separator: true },
      { name: 'cut', shortcut: 'mod+X',
        disabled: function() {return this.$project.scenario.selectedBlocks.length == 0},
        action: function() {this.$project.scenario.copy(true) }
       },
      { name: 'copy', shortcut: 'mod+C',
        disabled: function() {return this.$project.scenario.selectedBlocks.length == 0},
        action: function() {this.$project.scenario.copy() }
      },
      { name: 'paste', shortcut: 'mod+V',
        disabled: function() {return JSON.parse(localStorage.getItem('clipboard')) == null},
        action: function() {this.$project.scenario.paste() }
       },
      { name: 'remove', shortcut: 'delete',
        disabled: function() {return this.$project.scenario.selectedBlocks.length == 0},
        action: function() {this.$project.scenario.deleteSelected() }
      },
      { separator: true },
      { name: 'duplicate', shortcut: 'mod+D',
        disabled: function() {return this.$project.scenario.selectedBlocks.length == 0},
        action: function() {this.$project.scenario.duplicate() }
       },
      { separator: true },
      { name: 'edit', shortcut: 'mod+E',
        disabled: function() {return this.$project.scenario.selectedBlocks.length != 1},
        action: function() {this.$project.scenario.editingModel = this.$project.scenario.selectedBlocks[0] }
       },
      { separator: true },
      { name: 'select_all', shortcut: 'mod+A',
        action: function() {this.$project.scenario.selectAll() }
       },
      { name: 'select_nothing', shortcut: 'shift+mod+A', 
        action: function() {this.$project.scenario.selectedBlocks = [] }
       }
    ]
    },
    {
    name: 'display',
    items: [
      { name: 'sidebar_left', shortcut: 'mod+shift+L',
        checked: function() {return this.$project.sidebar.left},
        action: function() {this.$project.sidebar.left = !this.$project.sidebar.left}
       },
      { name: 'sidebar_right', shortcut: 'mod+shift+R',
        checked: function() {return this.$project.sidebar.right},
        action: function() {this.$project.sidebar.right = !this.$project.sidebar.right}
      },
      { separator: true },
      { name: 'grid',
        checked: function() {return this.$project.canvas.grid},
        action: function() {this.$project.canvas.grid = !this.$project.canvas.grid}
       },
      { separator: true },
      { name: 'boosters',
        checked: function() {return this.$project.display.boosters},
        action: function() {this.$project.display.boosters = !this.$project.display.boosters}
       },
      { name: 'booster_head',
        checked: function() {return this.$project.display.booster_info},
        disabled: function() {return !this.$project.display.boosters},
        action: function() {this.$project.display.booster_info = !this.$project.display.booster_info}
       },
      { name: 'losses', 
        checked: function() {return this.$project.display.losses},
        action: function() {this.$project.display.losses = !this.$project.display.losses},
        disabled: function() {return !this.$project.display.flows}
      },
      { name: 'flows',
        checked: function() {return this.$project.display.flows},
        action: function() {this.$project.display.flows = !this.$project.display.flows}
       },

      { separator: true },
      { name: 'zoom_in', shortcut: 'mod plus',
        disabled: function() {return this.$project.canvas.zoom >= 1.5},
        action: function() {this.zoom('in')}
       },
      { name: 'zoom_out', shortcut: 'mod minus' ,
        disabled: function() {return this.$project.canvas.zoom <= 0.25},
        action: function() {this.zoom('out')}
      },
      { name: 'zoom_fit',
        action: function() {this.$bus.emit('zoomFit')}
       },
      { separator: true },
      { name: 'fullscreen',
        action: function() {this.requestFullScreen()}
      },
      { separator: true},
      { name: 'debug',
        checked: function() {return this.$project.display.debug},
        action: function() {this.$project.display.debug = !this.$project.display.debug}
      }
    ]
  },
  {
    name: 'scenario',
    items: [
      { name: 'new', action: function() { this.addScenario()}},
      { name: 'duplicate', action: function() { this.addScenario(true)}},
      { name: 'remove', action: function() { this.removeScenario()}, disabled: function() {return this.$project.scenarios.length == 1}},
      { separator: true},
      { name: 'rename', action: function() { this.renameScenario()}},
      { separator: true},
    ]
  },
  {
    name: 'help',
    items: [
      { name: 'tutorial', action: function() {this.$project.tutorial = true} },
      { name: 'about', action: function() {}, disabled: () => true },
    ]
  }


]

export default {
  data() {
    return {
      submenu: false,
      menu: menu,
      submenuIndex: 0
    }
  },
  mounted() {
    this.$bus.on('removeScenario', () => {this.removeScenario() })
    this.$bus.on('addScenario', () => { this.addScenario() })
    this.$bus.on('duplicateScenario', () => { this.addScenario(true) })
    this.$bus.on('renameScenario', () => {this.renameScenario()})
  },
  methods: {
    removeScenario() {
      if (this.$project.scenarios.length <= 1) {
        return;
      }

      const options = {
        confirmButtonText: this.$t('ui.menubar.remove'),
        cancelButtonText: this.$t('ui.menubar.cancel'),
        type: 'warning',
      };

      ElMessageBox.confirm(this.$t('ui.menubar.confirm_remove'), this.$t('ui.menubar.remove_scenario') , options)
        .then(() => this.$project.removeScenario(this.$project.selectedScenario))
        .catch(() => {});
    },
    renameScenario() {

      this.promptForScenario(this.$t('ui.menubar.rename_scenario'), this.$t('ui.menubar.rename'), this.$project.scenarios[this.$project.selectedScenario].name)
        .then(({ value }) => this.$project.renameScenario(value))
        .catch(() => {});
    },

    addScenario(duplicate = false) {

      var newName = duplicate ? `${this.$project.scenarios[this.$project.selectedScenario].name} - kopie` : '';

      this.promptForScenario(this.$t('ui.menubar.new_scenario'), this.$t('ui.menubar.add_scenario'), newName, true)
        .then(({ value }) => this.$project.addScenario(value, duplicate))
        .catch(() => {});
    },
    promptForScenario(actionTitle, buttonText, defaultInput = '', create = false) {

      // get list of existing scenario names, except the current one if not creating
      const existingScenarios = this.$project.scenarios
        .filter((scenario, idx) => (idx !== this.$project.selectedScenario || create))
        .map((scenario) => scenario.name);



      return ElMessageBox.prompt(this.$t('ui.menubar.enter_scenario_name'), actionTitle, {
        inputValue: defaultInput,
        confirmButtonText: buttonText,
        cancelButtonText: this.$t('ui.menubar.cancel'),
        inputPattern: /\S+/,
        inputErrorMessage: this.$t('ui.menubar.enter_scenario_name_empty_error'),
        inputValidator: (inputValue) => {
          if (existingScenarios.includes(inputValue)) {
            return this.$t('ui.menubar.enter_scenario_name_already_exists'); // returns error message if the name exists already
          }
          return true;
        },
      });
    },
    getItems(item) {
      if(item.name == 'scenario') {
        // add scenarios
        var scenarios = this.$project.scenarios.map((scenario, idx) => {
          return {
            name: scenario.name,
            notranslate: true,
            checked: function() {return idx == this.$project.selectedScenario},
            action: function() {this.$project.selectScenario(idx)}
          }
        })
        return item.items.concat(scenarios)

      }
      return item.items
    },
    rename() {
      this.$prompt(this.$t('ui.topbar.rename_project'), this.$t('ui.topbar.rename_project_title'), {
        confirmButtonText: this.$t('ui.topbar.rename'),
        cancelButtonText: this.$t('ui.topbar.cancel'),
        inputValue: this.$project.name,
        inputPattern: /\S/,
        inputErrorMessage: this.$t('ui.topbar.rename_error')
      }).then(({ value }) => {
        this.$project.name = value
      }).catch(() => {})
    },
    // TODO: move to canvas
    zoom(direction) {
      let dz = direction == 'in' ? 0.2 : -0.2
      // apply bounds of 0.25 and 1.5
      let nz = this.$project.canvas.zoom + dz
      nz = Math.min(1.5, Math.max(0.25, nz))

      this.$bus.emit('setZoom', nz)
    },
    isDisabled(item) {
      return typeof item.disabled === 'function' ? item.disabled.bind(this)() : item.disabled;
    },
    handleAction(item) {
      if (this.isDisabled(item)) { return }
      if (item.action) {
        item.action.bind(this)()
      }
      this.closeSubmenu()
    },
    shortcut(shortcut) {
      let modified = navigator.platform.indexOf('Mac') > -1 ? '⌘' : 'Ctrl'
      return shortcut.replace('mod', modified).replace('shift', '⇧').replace('plus', '+').replace('minus', '-')
    },
    toggleSubmenu(evt) {
      evt.stopPropagation()

      if(this.submenu && !evt.target.classList.contains('main-item')) { return }
      this.submenu = !this.submenu
      if (this.submenu) {
        document.addEventListener('click', this.closeSubmenu)
      }
    },
    closeSubmenu() {
      this.submenu = false
      document.removeEventListener('click', this.closeSubmenu)
    },
    requestFullScreen() {
      var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
        (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
        (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
        (document.msFullscreenElement && document.msFullscreenElement !== null);

      if(isInFullScreen) {
        var exit = document.exitFullscreen || document.webkitExitFullscreen || document.mozCancelFullScreen || document.msExitFullscreen
        if (typeof exit != 'undefined' && exit) {
          exit.call(document)
        }
      }
      var el = document.documentElement
      var rfs = el.requestFullScreen || el.webkitRequestFullScreen || el.mozRequestFullScreen || el.msRequestFullScreen
      if (typeof rfs != 'undefined' && rfs) {
        rfs.call(el)
      }
    },
    requestNew() {
      ElMessageBox.confirm(
        this.$t('ui.menubar.new.confirm'), 
        this.$t('ui.menubar.new.title'), {
          distinguishCancelAndClose: true,
          confirmButtonText: this.$t('ui.menubar.new.confirm_button'),
          cancelButtonText: this.$t('ui.menubar.new.cancel_button'),
        }
    ).then(() => {
      this.download()
      this.$project.newProject()
    }).catch((action) => {
      if (action == 'cancel') {
        this.$project.newProject()
      }
    })
    },
    upload() {
      // upload JSON file
      var input = document.createElement('input')
      input.type = 'file'
      input.accept = 'application/json'
      input.onchange = e => {
        var file = e.target.files[0]
        var reader = new FileReader()
        reader.onload = e => {
          console.log(e)
          localStorage.setItem('project', e.target.result)
          this.$project.open()

          this.$nextTick().then(() => {
            this.$bus.emit('zoomFit')
          })
        }
        reader.readAsText(file)
      }
      input.click()
    },
    download() {
      // download to JSON file
      var download = JSON.stringify(this.$project.serialize())
      var blob = new Blob([download], { type: 'application/json' })
      var url = URL.createObjectURL(blob)
      var a = document.createElement('a')
      a.href = url
      a.download = this.$project.name + '.json'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },

    
  }


}


</script>
<style>
#menu {
  height: 30px;
  display: flex;
  flex-direction: row;
  background-color: var(--el-color-primary-dark-2);
  padding-left: 10px;
  gap: 0px;
  color: #FFF;
  align-items: center;
  border-bottom: 1px solid #AAA;
}

#menu #main-menu {
  padding-right: 10px;
  display: flex;
  align-items: center;
  flex-direction: row;
  padding-left: 5px;
  font-size: 14px;
  font-weight: bold;
  color: var(--el-color-primary-light-9);
  margin: 0px;
  gap: 15px;
  list-style: none;
}
#menu menu > li {
  position: relative;
}

#menu menu > li > span {
  cursor: pointer;
  display: inline-block;
  border-radius: 2px;
  padding: 2px 10px;
}

#menu menu > li > span:hover {
  color: var(--el-color-primary-light-7);
  background-color: var(--el-color-primary);
}

#menu menu li ul {
  position: absolute;
  top: 25px;
  width: 250px;
  background: var(--el-bg-color-overlay);
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  margin: 0px;
  padding: 3px;
  z-index: 1000;
  box-shadow: var(--el-box-shadow-light);
}

#menu menu li ul::after {
  content: '';
  position: absolute;
  top: -5px;
  left: 10px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid var(--el-bg-color-overlay);
}

#menu menu li ul li {
  padding: 5px;
  position: relative;
  padding-left: 23px;
  color: var(--el-text-color-regular);
  font-weight: normal;
  margin: 0px;
  list-style-type: none;
  cursor: pointer;
}
#menu menu li ul li:not(.disabled):hover {
  background: #EEE;
}
#menu menu li ul li.separator {
  border-top: 1px solid #CCC;
  margin: 5px 0px;
  cursor: default;
  padding: 0px;
}
#menu menu li ul li.disabled {
  color: #CCC;
  cursor: default;
}
#menu .shortcut {
  float: right;
  color: #AAA;
  font-size: 13px;
  font-weight: normal;
  margin-right: 10px;
}
#menu .checked {
  position: absolute;
  color: #AAA;
  left: 5px;
}
#menu .saved {
  font-size: 13px;
  color: var(--el-color-primary-light-9);
}
#menu .version {
  font-size: 12px;
  color: var(--el-color-primary-light-9);
  position: absolute;
  right: 10px;
}
</style>
