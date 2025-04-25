<template>
  <div class="parameter">
    <template v-if="parameter_type(param) == 'number'">
      <el-form-item :label="$t('models.'+param.namespace+'.parameters.'+param.name)">
        <NumberInput v-model="value" :min="range[0]" :max="range[1]" :units="formatUnits(param.uom)" :integer="param.type == 'int'" />
      </el-form-item>
    </template> 
    <template v-else-if="parameter_type(param) == 'boolean'">
      <div class="parameter-boolean">
      <el-checkbox v-model="value" :label="$t('models.'+param.namespace+'.parameters.'+param.name)"/>
      </div>
    </template>
    <template v-else-if="parameter_type(param) == 'select'">
      <div class="parameter-select">
      <el-form-item :label="$t('models.'+param.namespace+'.parameters.'+param.name)">
        <el-radio-group v-model="value">
          <el-radio-button v-for="option in param.options" :value="option">{{ $t('models.'+param.namespace+'.parameters.options.'+option) }}</el-radio-button>
        </el-radio-group>
        <!-- <el-segmented :options="segmentedOptions(param)" v-model="values[param.name]" /> -->
      </el-form-item>
      </div>
    </template>
    <template v-else-if="parameter_type(param) == 'dropdown'">
      <div class="parameter-select">
        <el-form-item :label="$t('models.'+param.namespace+'.parameters.'+param.name)">
          <el-select v-model="value">
            <el-option v-for="option in param.options" :label="$t('models.'+param.namespace+'.parameters.options.'+option)" :value="option" />
          </el-select>
        </el-form-item>
      </div>
    </template>
    <template v-else-if="parameter_type(param) == 'percentage'">
      <div class="parameter percentage">
        <el-form-item :label="$t('models.'+param.namespace+'.parameters.'+param.name)">
          <el-slider v-model="percentage" :min="range[0]*100" :max="range[1]*100"></el-slider>
          <span class="value">{{ percentage }}%</span>
        </el-form-item>
      </div>
    </template>
  </div>
</template>
<script>
import NumberInput from './NumberInput.vue'

export default {
  components: {NumberInput},
  props: ['param', 'modelValue', 'range'],
  data() {
    return {
      value: this.modelValue,
      percentage: this.modelValue * 100
    }
  },
  mounted() {
    this.value = this.modelValue
    this.percentage = this.modelValue * 100
  },
  watch: {
    range() {
      // clip value to range
      if (this.value < this.range[0]) {
        this.value = this.range[0]
      }
      if (this.value > this.range[1]) {
        this.value = this.range[1]
      }
    },
    percentage() {
      this.value = this.percentage / 100
    },
    value() {
      this.$emit('update:modelValue', this.value)
    },
    modelValue() {
      this.value = this.modelValue
    }
  },
  methods: {
    segmentedOptions(param) {
      return param.options.map(o => {
        return {label: this.$t('models.'+param.namespace+'.parameters.options.'+o), value: o}
      })
    },
    parameter_type(param) {

      if (param.options) {
        if (param.options.length > 4) {
          return 'dropdown'
        }
        else {
          return 'select'
        }
      }
      if (param.uom == '%') {
        return 'percentage'
      }

      let type = typeof param.default
      return type
    },
    formatUnits(uom) {
      if (uom === undefined) { return '-' }
      // wrap numbers in superscript, except for H2O, wrap in subscript
      if (uom.match(/H2O/)) return uom.replace(/(\d+)/g, '<sub>$1</sub>');

      return uom.replace(/(\d+)/g, '<sup>$1</sup>');
    },

  }
}

</script>
<style>
.parameter .el-input__inner {
  min-width: 20px;
}
</style>