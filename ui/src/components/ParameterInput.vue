<template>
  <div id="parameter-input">
  <el-tabs tab-position="left" v-model="activeTab">
    <el-tab-pane v-for="sections, category in parameters" :id="'category-'+category" :name="category">
      <template #label>
        <el-icon size="24px">
          <template v-if="icons[category].includes('fa')">
            <i class="fa tab" :class="icons[category]"></i>
          </template>
          <component :is="icons[category]" v-else/></el-icon>
          
          <span>{{ $t("ui.design.categories."+category) }}</span>
      </template>
      <el-form label-position="top" @submit.prevent size="default">
      <div v-for="params, section in nonempty(sections)" :id="'section-'+section" class="parameter-section">
        <h3>{{ $t('ui.design.sections.'+section)}}</h3>
        <div class="parameter-group">
          <Parameter v-for="param in filtered(params)" :param="param" v-model="values[param.name]" :key="param.name" :range="getRange(param)" :warning="paramWarning(param)"/>
        </div>
      </div>
      </el-form>
    </el-tab-pane>
    <component :is="'edit-'+editingModel.type" v-model="editingModel.configuration" v-if="customEditVue"></component>

  </el-tabs>
  </div>

</template>
<script>
// import Vue from 'vue'
import { resolveDynamicComponent } from 'vue'
import Parameter from './Parameter.vue'

export default {
  components: {
    Parameter
  },
  props: ['modelValue', 'type', 'uid'],
  data() { return {
    icons: {
      'design': 'Tools',
      'chemicals': 'Filter',
      'operational': 'Odometer',
      'model': 'Help',
      'gas_processing': 'fa-fire'
    },
    activeTab: 'design',
    editVue: false,
    percentages: {},
    values: {},
    customEditVue: false,
  }},
  created() {
    // load parameters
    this.values = _.cloneDeep(this.modelValue)
    var component = resolveDynamicComponent('edit-'+this.type)
    if (typeof component == 'object') {
      this.customEditVue = true
    }
    console.log("Editing", this.editingModel.configuration)
  },
  watch: {
    uid() {
      this.values = _.cloneDeep(this.modelValue)
      // check if the active tab is still valid
      if(!Object.keys(this.parameters).includes(this.activeTab)) {
        this.activeTab = Object.keys(this.parameters)[0]
      }
      this.activeTab = 'design'
      var component = resolveDynamicComponent('edit-'+this.type)
      if (typeof component == 'object') {
        this.customEditVue = true
      } else {
        this.customEditVue = false
      }
    },
    values() {
      this.$emit('update:modelValue', this.values)
    },
    percentages: {
      handler() {
        for(var p in this.percentages) {
          this.values[p] = this.percentages[p] / 100
        }
      },
      deep: true
    }
  },

  beforeUnmount() {
    this.customEditVue = false
  },
  methods: {
    getRange(param) {
      var calculatedRange = []
      if(!param.range) { return [0,100] }

      // if range is a string, it refers to another parameter
      for(var i in param.range) {
        if (typeof param.range[i] == 'string') {
          calculatedRange.push(this.values[param.range[i]])
        } else {
          calculatedRange.push(param.range[i])
        }
      }

      return calculatedRange
    },
    nonempty(sections) {
      let resp = {}
      for(var s in sections) {
        if (this.filtered(sections[s]).length > 0) {
          resp[s] = sections[s]
        }
      }
      return resp
    },
    filtered(params) {
      return params.filter(p => {
        if (p.hidden) { return false}
        if (p.if == undefined) { return true }
        // check if parameter is enabled
        if (p.if.or) {
          return Object.keys(p.if.or).some(k => this.checkCondition(this.values[k],p.if.or[k]))
        }
        return Object.keys(p.if).every(k => this.checkCondition(this.values[k],p.if[k]))
      })
    },
    checkCondition(value, condition) {
      if (condition instanceof Array) {
        switch(condition[0]) {
          case 'gt':
            return value > condition[1]
          case 'lt':
            return value < condition[1]
          case 'eq':
            return value == condition[1]
          case 'ne':
            return value != condition[1]
          case 'ge':
            return value >= condition[1]
          case 'le':
            return value <= condition[1]
        }
        return condition.includes(value)
      } else {
        return value == condition
      }
    },
    paramWarning(param) {
      if (this.type !== 'activatedcarbon') return ''
      const staggering =
        this.values.staggered_replacement === 'limit_staggering' ||
        this.values.staggered_replacement === 'fixed_staggering'
      const needsMoreUnits = staggering && Number(this.values.units) < 2
      if (needsMoreUnits && (param.name === 'staggered_replacement' || param.name === 'units')) {
        return this.$t('models.activatedcarbon.parameters.staggered_replacement_units_warning')
      }
      return ''
    },
  },
  computed: {
    customEdit() {
      return this.customEditVue && this.editingModel
    },
    editingModel() {
      var mdl = this.$project.scenario.models.find(m => m.uid == this.$project.scenario.editingModel)
      return mdl
    },
    parameters() {
      var params = this.$project.modelParameters[this.type]
      var parameters = {}
      // process parameters, split per category and section
      for(var p of params) {
        // skip hidden categories (starting with _)
        if(p.category.startsWith('_')) { continue }
        if(p.hidden) { continue }
        parameters[p.category] = parameters[p.category] || {}
        parameters[p.category][p.section] = parameters[p.category][p.section] || []
        parameters[p.category][p.section].push(p)
        if (this.values[p.name] === undefined) {
          this.values[p.name] = p.default // set default value
        }
        if (p.uom == '%') {
          this.percentages[p.name] = this.values[p.name] * 100
        }
      }
      return parameters
    }
  },
}
</script>
<style>
#parameter-input {
  display: flex;
}
#parameter-input .fa {
  width: 22px;

} 

#parameter-input .parameter-section {
  margin-bottom: 10px;
}

#parameter-input .el-form-item {
  margin-bottom: 8px;
}

#parameter-input h3 {
  font-size: 16px;
  margin-bottom: 8px;
}

#parameter-input .el-form-item__label {
  font-size: 14px;
  margin-bottom: 3px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

#parameter-input .el-input-group__append {
  font-size: 12px;
  height: 32px;
  width: 50px;
  padding: 0px;
  color: #333;
}
#parameter-input .el-input-group__append sup {
  font-size: 9px;
}

#parameter-input .parameter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0px 8px;
}
#parameter-input .parameter {
  flex: 1 1;
}

#parameter-input .parameter-boolean {
  width: 300px;
  padding-bottom: 5px;
}
#parameter-input .parameter-select {
  min-width: 250px;
  max-width: 300px;
}
#parameter-input .percentage {
  display: flex;
}
#parameter-input .el-slider {
  width: 230px;
  margin-left: 8px;
  padding-right: 15px;
}
#parameter-input .value {
  display: inline-block;
  width: 50px;
  text-align: center;
  font-size: 14px;
  margin-left: 0px;
}

</style>