<template>
  <div id="topbar">
    <MenuBar></MenuBar>
    <div id="buttonbar">
      <div class="left">
      <div class="toggle-left-sidebar" @click="$project.sidebar.left = !$project.sidebar.left" :class="{hidden: !$project.sidebar.left}"></div>
      <el-dropdown trigger="click">
        <el-button size="small" class="zoombutton">
          {{ Math.ceil($project.canvas.zoom * 100) }} %
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="$bus.emit('zoomFit')" :disabled="!zoomFitEnabled">{{ $t('ui.topbar.zoom_to_fit') }}</el-dropdown-item>
            <el-dropdown-item @click="setZoom(0.25)" divided>25%</el-dropdown-item>
            <el-dropdown-item @click="setZoom(0.5)">50%</el-dropdown-item>
            <el-dropdown-item @click="setZoom(0.75)">75%</el-dropdown-item>
            <el-dropdown-item @click="setZoom(1)">100%</el-dropdown-item>
            <el-dropdown-item @click="setZoom(1.25)">125%</el-dropdown-item>
            <el-dropdown-item @click="setZoom(1.5)">150%</el-dropdown-item>
          </el-dropdown-menu>
        
        </template>
      </el-dropdown>

      <el-button-group>
        <el-button size="small" @click="zoom('in')">
          <i class="fa fa-search-plus"></i>
        </el-button>
        <el-button size="small" @click="zoom('out')">
          <i class="fa fa-search-minus"></i>
        </el-button>
      </el-button-group>

      <el-button-group>
        <el-button size='small' @click="$project.$undo" :disabled="$project.undoStack.length == 0"><i class='fa fa-undo'></i></el-button>
        <el-button size='small' @click="$project.$redo" :disabled="$project.redoStack.length == 0"><i class='fa fa-repeat'></i></el-button>
      </el-button-group>

      <el-radio-group size="small" v-model="$project.mouseMode">
        <el-radio-button value="select"><i class='fa fa-mouse-pointer'></i></el-radio-button>
        <el-radio-button value="pan"><i class='fa fa-arrows'></i></el-radio-button>
      </el-radio-group>

      <el-select size='small' v-model="$i18n.locale" class="locale-select">
        <el-option v-for="locale in $i18n.availableLocales" :key="locale" :label="locale.toUpperCase()" :value="locale" />
      </el-select>
      
      </div>
      <div class="title">
          <i class="fa fa-file-o"></i>&nbsp;
          <span class='project-name' @click="rename">
          {{ $project.name }}<span v-if="$project.unsaved" class="unsaved">*</span>
          </span>
      </div>
      <div class="right">
        <el-button size="small" @click="feedback" type="info" plain class="feedback-button"><i class='fa fa-comment'></i>&nbsp;{{ $t('ui.topbar.feedback') }}</el-button>

        <el-badge :value="$project.number_of_overwrites" :max="10" class="solve-project" :hidden="$project.number_of_overwrites == 0">
          <el-button size="small" @click="$project.edit_key_figures" type="primary" plain class="solve-project"><i class='fa fa-database'></i>&nbsp;{{ $t('ui.topbar.key_figures') }}</el-button>
        </el-badge>
        <el-button size="small" @click="$project.run_report" type="success" plain class="solve-project"><i class='fa fa-flash'></i>&nbsp; {{ $t('ui.topbar.run_project') }}</el-button>

        <div class="toggle-fullscreen" @click="toggleFullscreen" :class="{fullscreen: !$project.sidebar.right && !$project.sidebar.left}"></div>

        <div class="toggle-right-sidebar" @click="$project.sidebar.right = !$project.sidebar.right" :class="{hidden: !$project.sidebar.right}"></div>
      </div>

    </div>
  </div>
</template>
<script>
import MenuBar from './MenuBar.vue'

export default {
  components: {
    MenuBar
  },
  data() { return {
    locale: 'EN'
  }},
  computed: {
    zoomFitEnabled() {
      return this.$project.scenario.models.length > 0
    }
  },
  methods: {
    feedback() {
      // send email to amanzi@vitens.nl
      // serialize the project and add it to the body
      let body = `%0D%0A%0D%0A%0D%0A====================Projectgegevens=========================== %0D%0A%0D%0A`
      body += btoa(JSON.stringify(this.$project.serialize()))
      window.open(`mailto:amanzi@vitens.nl?body=${body}`);
    },
    toggleFullscreen() {
      if(this.$project.sidebar.right || this.$project.sidebar.left) {
        this.$project.sidebar.right = false
        this.$project.sidebar.left = false
      } else {
        this.$project.sidebar.right = true
        this.$project.sidebar.left = true
      }
    },

    zoom(direction) {
      let dz = direction == 'in' ? 0.2 : -0.2
      // apply bounds of 0.25 and 1.5
      let nz = this.$project.canvas.zoom + dz
      nz = Math.min(1.5, Math.max(0.25, nz))

      this.$bus.emit('setZoom', nz)
    },
    setZoom(z) {
      this.$bus.emit('setZoom', z)
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
    }

  }


}

</script>
<style>
#topbar {
  display: flex;
  flex-direction: column;
}
#buttonbar {
  padding: 6px 15px;
  background: #FAFAFA;
  display: flex;
}
#buttonbar .left, #buttonbar .right {
  display: flex;
  align-items: center;
  gap: 10px;
}

#buttonbar .title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
}
#buttonbar .title .project-name:hover {
  cursor: pointer;
  text-decoration: underline;
}

#buttonbar .toggle-left-sidebar, #buttonbar .toggle-right-sidebar, #buttonbar .toggle-fullscreen {
  display: inline-block;
  width: 12px;
  height: 12px;
  cursor: pointer;
  opacity: 0.8;
}
#buttonbar .toggle-left-sidebar:hover, #buttonbar .toggle-right-sidebar:hover, #buttonbar .toggle-fullscreen:hover {
  opacity: 1;
}
#buttonbar .el-radio-group {
  margin-right: 10px;
}
#buttonbar .el-radio-group label span {
  height: 24px !important;
}
#buttonbar .toggle-fullscreen {
  background: url('@/assets/fullscreen.png') no-repeat;
  background-size: contain;
  margin-right: 10px;
  margin-left: 10px;
  cursor: pointer;
}
#buttonbar .toggle-fullscreen.fullscreen {
  background: url('@/assets/fullscreen-off.png') no-repeat;
  background-size: contain;
}
#buttonbar .toggle-left-sidebar {
  background: url('@/assets/sidebar-left-on.png') no-repeat;
  background-size: contain;
}
#buttonbar .toggle-right-sidebar {
  background: url('@/assets/sidebar-right-on.png') no-repeat;
  background-size: contain;
}
#buttonbar .toggle-left-sidebar.hidden {
  background: url('@/assets/sidebar-left-off.png') no-repeat;
  background-size: contain;
}
#buttonbar .toggle-right-sidebar.hidden {
  background: url('@/assets/sidebar-right-off.png') no-repeat;
  background-size: contain;
}
.el-dropdown {
  margin-left: 10px;
  margin-right: 10px;
}
.el-button-group {
  margin-right: 10px;
}
.zoombutton {
  width: 60px;
}
.toggle-sidebar {
  float: right;
}

.locale-select {
  padding-left: 0px;
  width: 60px !important;
}
.solve-project {
  float: right;
}

#buttonbar .el-badge sup {
  top: 1px;
  right: 18px;
  font-size: 10px;
  font-weight: bold;
  padding: 0px 6px;
}

</style>