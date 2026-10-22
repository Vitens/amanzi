<template>
  <number-input
    :model-value="displayValue"
    @update:model-value="onInput"
    v-bind="$attrs"
  />
</template>

<script>
const UNIT_FACTORS = { 'ng/l': 1, 'μg/l': 1000, 'mg/l': 1000000 }

export default {
  name: 'UnitNumberInput',
  inheritAttrs: false,
  props: {
    modelValue: { type: Number, default: 0 },
    unit: { type: String, default: 'ng/l' },
  },
  emits: ['update:modelValue'],
  computed: {
    factor() {
      return UNIT_FACTORS[this.unit || 'ng/l'] ?? 1
    },
    displayValue() {
      return (this.modelValue ?? 0) / this.factor
    },
  },
  methods: {
    onInput(val) {
      this.$emit('update:modelValue', val * this.factor)
    },
  },
}
</script>
