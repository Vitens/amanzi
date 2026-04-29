<template>
  <svg>
    <path :d="pipeline" fill="#EEE" stroke="black" stroke-width="2" />
  </svg>
</template>

<script>
import hydraulicLine from '@/mixins/hydraulicline'

export default {
  mixins: [hydraulicLine],
  name: 'hydraulic-pipeline',
  props: ['model'],
  computed: {
    anchorpoints() {
      return {
        in: { x: this.x0, y: this.y(-0.4), anchor: 'left' },
        out: { x: this.x0 + this.width, y: this.y(-0.4), anchor: 'right' }
      }
    },
    pipeline() {
      return this.rect(this.x0, this.y(-0.3), this.width, this.y(-0.3) - this.y(-0.5))
    }
  }
}
</script>