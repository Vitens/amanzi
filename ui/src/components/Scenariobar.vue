<template>
  <div id="scenarios" ref="scenarios">
    <div class="scenario-scroll-zone">
      <button
        type="button"
        class="scroll-arrow scroll-arrow-left"
        aria-label="Scroll scenarios left"
        :class="{ visible: canScrollLeft }"
        @click="scrollLeft"
      >
        <i class="fa fa-chevron-left"></i>
      </button>
      <div class="scenario-list-wrapper" ref="scenarioListWrapper" @scroll="onScroll">
        <ul class="scenario-list" ref="scenario-list">
          <li v-for="scenario, idx in $project.scenarios"
              :key="scenario.uid"
              :class="{ active: idx == $project.selectedScenario, 'just-added': idx === $project.lastAddedScenarioIndex }"
              @click="$project.selectScenario(idx)"
              @dblclick="renameScenario"
              :data-idx="idx"
              >
              {{ scenario.name }} <i class='fa fa-ellipsis-v scenario-options' v-show="idx == $project.selectedScenario" @click="showMenu"></i></li>
        </ul>
      </div>
      <button
        type="button"
        class="scroll-arrow scroll-arrow-right"
        aria-label="Scroll scenarios right"
        :class="{ visible: canScrollRight }"
        @click="scrollRight"
      >
        <i class="fa fa-chevron-right"></i>
      </button>
    </div>
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
  data() {
    return {
      canScrollLeft: false,
      canScrollRight: false
    }
  },
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
    this.$nextTick(() => {
      this.updateScrollState()
      this.scrollActiveIntoView()
    })
  },
  updated() {
    this.$nextTick(() => this.updateScrollState())
  },
  watch: {
    '$project.selectedScenario'() {
      this.$nextTick(() => this.scrollActiveIntoView())
    }
  },
  methods: {
    scrollActiveIntoView() {
      const list = this.$refs['scenario-list']
      const idx = this.$project?.selectedScenario
      if (!list || idx == null || !list.children[idx]) return
      list.children[idx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' })
    },
    updateScrollState() {
      const el = this.$refs.scenarioListWrapper
      if (!el) return
      this.canScrollLeft = el.scrollLeft > 0
      this.canScrollRight = el.scrollLeft < el.scrollWidth - el.clientWidth - 1
    },
    onScroll() {
      this.updateScrollState()
    },
    scrollLeft() {
      const el = this.$refs.scenarioListWrapper
      if (!el) return
      el.scrollBy({ left: -200, behavior: 'smooth' })
    },
    scrollRight() {
      const el = this.$refs.scenarioListWrapper
      if (!el) return
      el.scrollBy({ left: 200, behavior: 'smooth' })
    },
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
  border-top: 1px solid #333;
  height: 45px;
  min-height: 45px;
  display: flex;
  align-items: stretch;
  overflow: hidden;
}
.scenario-scroll-zone {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: stretch;
  position: relative;
}
.scroll-arrow {
  flex-shrink: 0;
  width: 28px;
  border: none;
  background: rgba(0, 0, 0, 0.06);
  color: #666;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s, background 0.2s;
  z-index: 1;
}
.scroll-arrow.visible {
  opacity: 1;
}
.scenario-scroll-zone:hover .scroll-arrow.visible {
  opacity: 0.85;
}
.scroll-arrow.visible:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.1);
}
.scroll-arrow i {
  font-size: 12px;
}
.scenario-list-wrapper {
  flex: 1;
  min-width: 0;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
}
.scenario-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: nowrap;
  height: 100%;
}
.scenario-list li {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  padding: 11px 20px;
  color: #666;
  background-color: #EEE;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
  border-left: 1px solid #999;
  transition: all 0.3s;
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

/* brief highlight when scenario was just added (new or duplicate) */
.scenario-list li.just-added {
  animation: scenario-added-pulse 0.9s ease-out;
}
@keyframes scenario-added-pulse {
  0% { background-color: #E8F4FF; box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.35); }
  50% { background-color: #D6EBFF; box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.2); }
  100% { background-color: #FFF; box-shadow: none; }
}
.scenario-list li.just-added.active {
  animation: scenario-added-pulse-active 0.9s ease-out;
}
@keyframes scenario-added-pulse-active {
  0% { background-color: #D6EBFF; box-shadow: inset 0 0 0 2px rgba(64, 158, 255, 0.4); }
  50% { background-color: #E8F4FF; box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.25); }
  100% { background-color: #FFF; box-shadow: none; }
}
.scenario-options {
  color: #999;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
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
  bottom: 49px;
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
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 45px;
  height: 45px;
  border: none;
  border-left: 1px solid #CCC;
  font-size: 16px;
  color: #666;
  background: #F5F7FA;
  cursor: pointer;
  transition: color 0.2s, background 0.2s;
}
.add-scenario:hover {
  color: #409EFF;
  background: #E8F4FF;
}
.sorting {
  background: red;
}

</style>