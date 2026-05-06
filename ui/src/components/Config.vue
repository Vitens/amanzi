<template>
  <div id="config">
    <!-- element ui form with labels on top of the inputs -->
    <el-form label-position="top" v-if="showConfig" @submit.prevent>
      <el-form-item :label="$t('ui.sidebar.configuration.name')">
        <el-input v-model="editingModel.name"></el-input>
      </el-form-item>

      <Parameter v-for="param in parameters" :key="param.name" :param="param" v-model="editingModel.configuration.parameters[param.name]" :range="param.range" />

      <el-button type="primary" @click="$project.scenario.editingModel = editingModel.uid" icon="Edit" class="edit_button" :disabled="editDisabled">{{ $t('ui.sidebar.configuration.edit') }}</el-button>
    </el-form>

  </div>
</template>
<script>

import { watch } from 'vue'
import Parameter from './Parameter.vue';
import _ from 'lodash'

export default {
  components: { Parameter },
  name: 'Config',
  data() { return {
    showConfig: false,
    editingModel: {},
    initialize: false,
    minorloss: 0,
    minorloss_method: 'percentage'
  }},
  mounted() {

    // update editing model when selected model changes
    this.$bus.on('selection-changed', () => {
      const selection = this.$project.scenario.selectedBlocks


      if(selection.length == 1) {
        // watch changes
        
        // make a copy of the model
        this.showConfig = true
        this.editingModel = this.$project.scenario.models.find(m => m.uid == selection[0])

        // cancel previous watch
        if(this.$options.unwatch) {
          this.$options.unwatch()
        }
        this.initialize = this.$project.scenario.unsaved

        this.$options.unwatch = watch(this.editingModel.configuration, (val) => {
          this.$project.scenario.unsolved = true
          this.$project.scenario.unsaved = this.initialize
          this.initialize = true
        }, { deep: true })

      } else {
        // clear editing model if multiple models selected
        if(this.$options.unwatch) {
          this.$options.unwatch()
        }
        this.showConfig = false
        this.editingModel = {}
      }
    })
  },
  computed: {
    editDisabled() {
      return !this.$project.scenario.validate().valid
    },
    parameters() {
      // get quick parameters from the model
      return this.$project.modelParameters[this.editingModel.type].filter(p => p.quick)
    }
  }

}
</script>
<style>
#config .el-input-group__append {
  width: 50px;
}
#config .edit_button {
  width: 100%;
  margin-top: 10px;
}
#config .percentage {
  width: 100%;
}
</style>