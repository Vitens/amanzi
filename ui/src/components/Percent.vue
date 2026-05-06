<template>
  <el-form-item :label="label">

    <el-slider v-model="percentage" :min="0" :max="max" :step="1" v-if="slider"></el-slider>

    <el-input type="number" v-model="percentage" :min="0" :max="max" v-else>
      <template #append>
        &percnt;
      </template>
    </el-input>
  </el-form-item>

</template>
<script>
import { watch } from 'vue';

export default {
  props: {
    'modelValue': {
      type: Number,
      default: 0
    },
    'label': {
      type: String,
      default: 'Percentage'
    },
    'max': {
      type: Number,
      default: 100
    },
    'slider': {
      type: Boolean,
      default: false
    },
  },
  data() { return {
    percentage: 0
  }},
  mounted() {
    this.percentage = this.modelValue * 100
  },
  watch: {
    modelValue(val) {
      this.percentage = val * 100
    },
    percentage(val) {
      this.$emit('update:modelValue', val / 100)
    }
  }
}


</script>