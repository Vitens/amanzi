<template>
  <g>
    <circle :cx="x0 + width/2" :cy="y(booster_elevation)" :r="radius" stroke="#000" fill="white" stroke-width="2" />
    <path :d="trianglePath" stroke="#000" fill="#000" stroke-width="2" />
    <rect :x="x0 + width/2 - 25" :y="y(booster_elevation) - 39" :width="50" :height="16" fill="orange" stroke="#333" stroke-width="2" />
    <text :x="x0 + width/2" :y="y(booster_elevation) - 27" font-size="11" text-anchor="middle">{{ format(config.booster_head) }}</text>
  </g>
</template>

<script>
import HydraulicLine from '@/mixins/hydraulicline.js'

export default {
  mixins: [HydraulicLine],
  props: ['config', 'dim', 'offset', 'width', 'suggestedElevation', 'uid'],

  data() {
    return {
      radius: 15
    }
  },
  methods: {
    format(value) {
      if(value == undefined) return '?.? m'
      return '+' + value.toFixed(1) + ' m'
    }
  },

  computed: {
    booster_elevation() {
      return this.config.elevation != undefined ? this.config.elevation : this.suggestedElevation
    },
    anchorpoints() {
      return {
        in: {x: this.x0 + this.width/2 - this.radius, y: this.y(this.booster_elevation), anchor: 'left'},
        out: {x: this.x0 + this.width/2 + this.radius, y: this.y(this.booster_elevation), anchor: 'right'}
      }
    },
    trianglePath() {
      // draw triangle with point to the right
      return this.triangle(this.x0 + this.width/2, this.y(this.booster_elevation), this.radius-1, 90)
    },
    dimensions() {
      return {
        bottom: this.booster_elevation,
        top: this.booster_elevation
      }
    }
  }
}
</script>
