<template>
  <svg>
    <template v-if="params.integrated_booster">
      <circle :cx="this.x0 + 0.5 * this.width" :cy="this.y(params.inlet_elevation)" :r="radius"
        stroke="black" stroke-width="3" fill="white" />
      <path :d="trianglePath" stroke="black" fill="black" stroke-width="2" />
      <path :d="line" fill="#409EFF" stroke="#409EFF" stroke-width="2"></path>
      <rect :x="x0 + width/2 - 25" :y="y(elevation) - 39" :width="50" :height="16" fill="orange" stroke="#333" stroke-width="2" />
      <text :x="x0 + width/2" :y="y(elevation) - 27" font-size="11" text-anchor="middle">{{ format(hydraulics.booster_head) }}</text>
    </template>
    <path :d="distributionArrow" fill="#409EFF" stroke="#409EFF" stroke-width="4" stroke-linecap="round" />
  </svg>
</template>
<script>
import hydraulicLine from '@/mixins/hydraulicline'


export default {
  name: 'hydraulic-output',
  props: ['position', 'config', 'path', 'dim'],
  mixins: [hydraulicLine],
  data() {
    return {
      radius: 20
    }
  },
  methods: {
    format(value) {
      return '+' + value.toFixed(1) + ' m'
    }
  },
  computed: {
    levels() {
      return [{
        x: this.x0 + this.width * 0.8  ,
        y: this.y(this.params.inlet_elevation),
        level: this.params.required_pressure,
        direction: 'ne',
        pressure: true
      }]
    },
    elevation() {
      return this.params.inlet_elevation
    },
    anchorpoints() {
      if (!this.params.integrated_booster) {
        return {
          in: { x: this.x0+this.width, y: this.y(this.params.inlet_elevation), anchor: 'left' },
          out: { x: this.x0+this.width, y: this.y(this.params.inlet_elevation), anchor: 'right' },
        }
      }
      return {
        in: { x: this.x0+0.35*this.width, y: this.y(this.params.inlet_elevation), anchor: 'left' },
        out: { x: this.x0+0.35*this.width, y: this.y(this.params.inlet_elevation), anchor: 'right' },
      }
    },
    line() {
      // line from the booster to the inlet
      return `M ${this.x0 + 0.5*this.width + this.radius + 2} ${this.y(this.params.inlet_elevation)} L ${this.x0 + this.width} ${this.y(this.params.inlet_elevation)}`
    },
    trianglePath() {
      // draw triangle with point to the right
      return this.triangle(this.x0 + this.width/2, this.y(this.params.inlet_elevation), this.radius-1, 90)
    },
    connectorBooster() {
      let x = this.dim.width - 1 * this.r;
      let y = this.y(this.params.inlet_elevation);
      return `M ${x},${y} L ${this.dim.width},${y}`;
    },
    distributionArrow() {
      let x = this.x0 + this.width;
      let y = this.y(this.params.inlet_elevation);
      var path = `M ${x},${y + 0.05 * this.width} 
                        L ${x + 0.08 * this.width},${y} 
                        L ${x},${y - 0.05 * this.width} 
                        Z
                        `;
      return path;
    }
  }
}
</script>