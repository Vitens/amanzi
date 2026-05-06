<template>
  <svg>
    <!-- bottom cylinder -->
    <path :d="cylinder" fill="white" stroke="black" stroke-width="2" />
    <path :d="bottom" fill="white" stroke="black" stroke-width="2" />
    <path :d="funnel" fill="white" stroke="black" stroke-width="2" v-if="funneled" />
    <path :d="outlet" fill="white" stroke="black" stroke-width="2" />
    <path :d="water" fill="transparent" stroke="#409EFF" stroke-width="2" />
    <path :d="overflow" fill="white" stroke="black" stroke-width="2" />
  </svg>
</template>


<script>
import hydraulicLine from '@/mixins/hydraulicline'

export default {
  name: 'hydraulic-softening',
  
  mixins: [hydraulicLine],

  computed: {
    anchorpoints() {
      return {
        in: { x: this.cylinderX, y: this.y(this.params.inlet_elevation), anchor: 'left' },
        out: { x: this.x0 + 0.9*this.width+10, y: this.y(this.params.inlet_elevation + this.height)+10, anchor: 'bottom', booster: this.y(this.params.inlet_elevation + this.height - 1) }
      }
    },
    dimensions() {
      return {
        bottom: this.params.inlet_elevation,
        top: this.params.inlet_elevation + this.height
      }
    },
    funneled() {
      return this.params.reactor_shape == 'funnel'
    },
    height() {
      if (this.funneled) {
        return this.params.height_cylindrical + this.params.height_funnel
      }
      return this.params.height_cylindrical
    },

    funnelWidth() {
      return 0.8 * this.width
    },

    cylinderWidth() {
      if (this.funneled) {
        // get ratio between funnel and cylinder diameter
        let ratio = this.params.diameter_cylindrical / this.params.diameter_funnel
        return ratio * 0.8 * this.width
      }
      return 0.8 * this.width
    },

    cylinderX() {
      return this.x0 + this.width/2 - this.cylinderWidth/2
    },

    bottom() {
      let x0 = this.cylinderX
      let y0 = this.y(this.params.inlet_elevation) + this.length(0.25)
      let width = this.cylinderWidth
      let height = this.length(0.5)
      return this.rect(x0, y0, width, height)
    },
    
    // path for the cylindrical part of the softening reactor
    cylinder() {

      let x0 = this.cylinderX
      let y0 = this.y(this.params.inlet_elevation)
      let height = this.length(this.params.height_cylindrical)

      return this.rect(x0, y0, this.cylinderWidth, height)
    },
    // path for the funnel part of the softening reactor
    funnel() {
      let x0 = this.cylinderX
      let y0 = this.y(this.params.inlet_elevation + this.params.height_cylindrical)
      let width1 = this.funnelWidth
      let width2 = this.cylinderWidth
      let height = this.length(this.params.height_funnel)

      return this.trapezoid(x0, y0, width1, width2, height)
    },

    outlet() {
      let x0 = this.x0
      let height = this.params.reactor_shape == 'funnel' ? this.params.height_cylindrical + this.params.height_funnel : this.params.height_cylindrical

      let y0 = this.y(this.params.inlet_elevation + height)
      y0 += 10

      return this.rect(x0, y0, this.width, 25)
    },
    overflow() {
      let x0 = this.x0 + 0.1 * this.width
      let y0 = this.y(this.params.inlet_elevation + this.height)

      let path = `M ${x0} ${y0}`

      let zig = -2
      let n = 22
      for(var i = 0; i < n+1; i++) {
        let y = y0 + zig
        zig *= -1
        let w = x0 + i* (this.width*0.8)/n
        path += `L ${w} ${y}`
      }

      return path + this.rect(x0, y0+10, this.width*0.8, 25)
    },
    water() {
      let x0 = this.x0 + 1 // offset to avoid overlap with overflow
      let y0 = this.y(this.params.inlet_elevation + this.height)
      return this.line(x0, y0, x0 + this.width-2, y0)
    }

  },
}

</script>