<template>
  <el-input type="number" :min="min" :max="max" :step="cstep" v-model="numberValue" @blur="commitValue" @change="commitValue" :class="class" :placeholder="placeholder" :size="size">
    <template #append v-if="units != ''">
       <span v-html="units"></span>
    </template>
  </el-input>
  <span class="commit-message" v-if="numberValue != modelValue">{{$t('ui.general.press-enter-to-commit')}}</span>
</template>
<script>

export default {
  props: {
    min: { type: Number, default: 0 },
    max: { type: Number, default: 100 },
    integer: { type: Boolean, default: false },
    step: { type: Number, default: undefined },
    class : { type: String, default: ''},
    modelValue: { type: Number, default: 0 },
    size: { type: String, default: 'default' },
    units: {type: String, default: ''},
    placeholder: {type: String, default: ''},
  },
  emits: ['update:modelValue'],
  created() {
    this.numberValue = this.modelValue
  },
  watch: {
    modelValue() {
      this.numberValue = this.modelValue
    }
  },
  methods: {
    commitValue() {
      // clip to min/max value
      this.numberValue = Math.min(this.max, Math.max(this.min, this.numberValue))
      // if step is integer, round to nearest integer
      this.numberValue = this.integer ? Math.round(this.numberValue) : this.numberValue

      this.$emit('update:modelValue', this.numberValue)
    }
  },
  data() {
     return {
       numberValue: 0,
     }
  },
  computed: {
    cstep() {
      // if default is integer, return step as integer
      if (this.integer) {
        return 1
      }
      if (this.step === undefined) {

        if (this.max - this.min < 1) {
          return 0.01
        } else if (this.max - this.min < 10) {
          return 0.1
        } else {
          return 1
        }

      }
      return this.step
      
    }
  },
  name: 'NumericInput'

}

</script>
<style>
.numeric-input {
  position: relative;
}
.commit-message {
  position: absolute;
  font-size: 10px;
  color: #888;
  font-weight: bold;
  width: 150px;
  left: 50%;
  margin-left: -75px;
  bottom: -25px;
  

}

</style>