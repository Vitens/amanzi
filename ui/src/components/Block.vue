<template>
  <div
    :id="info.uid"
    ref="model"
    class="model"
    :class="blockClasses"
    v-draggable="{start: startMove, move, end: endMove, snap: 5, scale: true}"
    :style="{left: info.position.x + 'px', top: info.position.y + 'px'}"
    @mousedown="select"
    @dblclick="edit"
  >
    <el-icon :size="15" class="delete" @click="deleteBlock()"><delete /></el-icon>
    <div class="model-title">{{info.name}}</div>
    <div class="model-content">
      <component :is="'block-'+info.type" :model="info"></component>
    </div>
    <endpoint :uid="info.uid" :info="e" v-for="e in modelSpec.anchors" :key="info.uid+e.position" :connected="isConnected(e)"></endpoint>
    <div class="extended-info" v-if="debug">
      <label class="hydraulics_name">UID:</label>
      <span class="hydraulics_value">{{ info.uid }}</span>
      <div v-for="value, name in hydraulics" :key="name">
        <label class="hydraulics_name">{{ name }}</label>
        <span class="hydraulics_value">{{format(value)}}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { resolveDynamicComponent } from 'vue'
import draggable from '../directives/draggable.js'
import Endpoint from './Endpoint.vue'

export default {
  name: 'block',
  props: ['info'],
  components: { Endpoint },
  directives: {draggable},
  data() { return {
    hasDesignVue: false,
  }},
  mounted() {
    var component = resolveDynamicComponent('design-'+this.info.type)
    if (typeof component == 'object') {
      this.hasDesignVue = true
    }

    this.$nextTick(() => {
      // get dimensions of block
      this.sizeBlock()
    })
  },
  computed: {
    debug() {
      return this.$interface.display.debug
    },
    modelSpec() {
      return this.modelspec[this.info.type]
    },
    blockClasses() {
      var classes = [this.info.type]
      if(this.$project.scenario.selectedBlocks.includes(this.info.uid)) {
        classes.push('selected')
      }
      return classes
    },
    hydraulics() {
      if (this.$project.state.hydraulics && this.$project.state.hydraulics[this.info.uid]) {
        return this.$project.state.hydraulics[this.info.uid]
      }
    }
  },
  methods: {
    format(value) {
      try {
        return value.toFixed(2)
      } catch(e) {
        return value
      }
    },
    edit() {
      // check if design template for this model exists
      // if(!this.hasDesignVue) { return }
      if(!this.$project.scenario.validate().valid) { return }
      this.$project.scenario.unsolved = true
      this.$project.scenario.editingModel = this.info.uid
    },
    select(evt) {
      // if shift key pressed, append selection
      if(evt.shiftKey) {
        this.$project.scenario.selectBlock(this.info.uid, true)
      } else {
        this.$project.scenario.selectBlock(this.info.uid)
      }
      this.$bus.emit('selection-changed')
    },
    // Called when the user starts dragging the block
    startMove() {
      // Return true to allow dragging to continue
      this.$project.scenario.prepareMove()
      return true
    },
    isConnected(endpoint) {
      return this.$project.scenario.connections.some(c => (c.src == this.info.uid && c.srcAnchor == endpoint.position) || (c.tgt == this.info.uid && c.tgtAnchor == endpoint.position))
    },

    // Called when the user stops dragging the block
    endMove() {
      this.$project.scenario.commitMove()
    },

    // Called when the user moves the block
    move(dx, dy) {
      // Notify the store that the block has been moved
      this.$project.scenario.moveSelection(dx, dy)
    },

    // Called when the block is resized
    sizeBlock() {
      // Emit a "sized" event with the block's UID and dimensions
      this.$emit('sized', this.info.uid, this.$refs.model.clientWidth, this.$refs.model.clientHeight)
    },

    // Called when the user deletes the block
    deleteBlock() {
      // Notify the store to delete the block with the given UID
      this.$project.scenario.deleteBlock(this.info.uid)
    }
  }

}
</script>

<style>
.model {
  position: absolute;
  width: 100px;
  height: 100px;
  outline: 1px solid #333;
  background-color: #FFF;
  cursor: move;
  z-index: 10;
}

.model-title {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 16px;
  border-bottom: 1px solid #AAA;
  font-size: 12px;
  padding-top: 5px;
  background: #DDD;
  text-align: center;
  text-overflow: ellipsis;
  overflow: hidden;
}

.model:hover .delete {
  display: block;
}

.model .delete {
  background: #FFF;
  position: absolute;
  top: -5px;
  right: -5px;
  z-index: 11;
  fill: red;
  display: none;
  opacity: 0.5;
}

.model .delete:hover {
  cursor: pointer;
  opacity: 1;
}

.model.selected {
  outline: 2px solid #00F;
}

.model .extended-info {
  position: absolute;
  background: #FFF;
  padding: 3px;
  border: 1px dashed #AAA;
  bottom: 110px;
  width: 120px;
  font-size: 11px;
}
.model .extended-info label {
  display: inline-block;
  margin: 0;
  padding: 0;
  width: 85px;
  font-weight: bold;
}

</style>