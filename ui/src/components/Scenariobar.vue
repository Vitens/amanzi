<template>
  <div id="scenarios" ref="scenarios">
    <ul class="scenario-list" ref="scenario-list">
      <li v-for="scenario, idx in $project.scenarios" 
          :key="scenario.uid" 
          :class="{active: idx == $project.selectedScenario}" 
          @click="$project.selectScenario(idx)"
          @dblclick="renameScenario"
          :data-idx="idx"
          >
          {{ scenario.name }} <i class='fa fa-ellipsis-v scenario-options' v-show="idx == $project.selectedScenario" @click="showMenu"></i></li>

    </ul>

    <div @click="$bus.emit('addScenario')" class="add-scenario"><i class='fa fa-plus'></i></div>

    <ul id="scenario-menu" ref="menu">
      <li @click="$bus.emit('renameScenario')"><i class='fa fa-pencil-square-o'></i>{{ $t('ui.scenariobar.rename') }}</li>
      <li @click="$bus.emit('duplicateScenario')"><i class='fa fa-copy' ></i>{{ $t('ui.scenariobar.duplicate') }}</li>
      <li @click="$bus.emit('removeScenario')" :class="{removeDisabled: $project.scenarios.length == 1}"><i class='fa fa-remove'></i>{{ $t('ui.scenariobar.remove') }}</li>
    </ul>

  </div>

</template>
<script>
import { Sortable } from 'sortablejs'
import { ElMessageBox } from 'element-plus';

export default {
  mounted() {

    var doSort = function(evt) {
      this.$project.scenarios.splice(evt.newIndex, 0, this.$project.scenarios.splice(evt.oldIndex, 1)[0])

      if (evt.oldIndex == this.$project.selectedScenario) {
        this.$project.selectedScenario = evt.newIndex
      }

    }


    new Sortable(this.$refs['scenario-list'], {
      animation: 150,
      filter: '.add-scenario',
      ghostClass: 'sorting',
      onEnd: doSort.bind(this)
    })
  },
  methods: {
    showMenu(evt) {
      const menu = this.$refs.menu;

      const bounds = evt.target.getBoundingClientRect();
      const parentBounds = this.$refs.scenarios.getBoundingClientRect();
      const relativeLeft = bounds.left - parentBounds.left;

      Object.assign(menu.style, {
        display: 'block',
        left: `${relativeLeft - 10}px`,
      });
      document.addEventListener('click', this.hideMenu);
      evt.stopPropagation();
    },

    hideMenu() {
      this.$refs.menu.style.display = 'none';
      document.removeEventListener('click', this.hideMenu);
    },
  },
};
</script>
<style>
.scenarios {
  padding: 0px !important;
  background: #F5F7FA;
  position: relative;
}
#scenarios {
  /* background: #888; */
  border-top: 1px solid #333;
  height: 40px;
}
.scenario-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: inline-block;
}
.scenario-list li {
  display: inline-block;
  padding: 11px 20px;
  color: #666;
  background-color: #EEE;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
  border-left: 1px solid #999;
  transition: all 0.3s;
  /* transition: all 0.5s; */
}

.scenario-list li:hover {
  color: #333;
  /* color: #409EFF; */
}
.scenario-list li:first-child {
  border-left: none;
}
.scenario-list li:last-child {
  font-size: 14px;
  padding: 11px 10px;
  border-right: 1px solid #999;
}

.scenario-list li.active {
  position: relative;
  color: #409EFF;
  background: #FFF;
  padding-right: 30px;
  cursor: move;
}
.scenario-options {
  color: #999;
  position: absolute;
  top: 13px;
  right: 15px;
  padding: 0px 5px;
  cursor: pointer;
}
.scenario-options:hover {
  color: #409EFF;
}

#scenario-menu {
  position: absolute;
  list-style: none;
  padding: 0;
  margin: 0;
  background: #FFF;
  border: 1px solid #CCC;
  border-radius: 4px;
  box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);
  bottom: 34px;
  left: 440px;
  display: none;
}
#scenario-menu::after {
  content: '';
  position: absolute;
  bottom: -11px;
  left: 10px;
  border: 6px solid transparent;
  border-top: 6px solid white;
}
#scenario-menu::before {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 10px;
  border: 6px solid transparent;
  border-top: 6px solid #CCC;
}
#scenario-menu li {
  padding: 6px 10px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  width: 110px;
  transition: all 0.5s;
  border-bottom: 1px solid #EEE;
}
#scenario-menu li:last-child {
  border-bottom: none;
}

#scenario-menu li:hover {
  background: #F5F7FA;
  color: #333;
}

#scenario-menu i {
  margin-right: 10px;
}

#scenario-menu li.removeDisabled {
  color: #CCC;
  cursor: default;
}
#scenario-menu li.removeDisabled:hover {
  background: #FFF;
  color: #CCC;
}

.add-scenario {
  display: inline-block;
  width: 100px;
  border-left: 1px solid #FFF;
  padding-left: 10px;
  font-size: 13px;
}
.add-scenario :hover {
  color: #409EFF;
  cursor: pointer;
}
.sorting {
  background: red;
}

</style>