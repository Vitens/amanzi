<template>
  <g>
    <path :d="level_triangle" fill="white" stroke="#F56C6C" stroke-width="2" v-if="!pressure"/>

    <template v-else>
      <path :d="level_line" fill="white" stroke="#F56C6C" stroke-width="2" />
      <circle :cx="cx" :cy="cy" r="3" fill="#F56C6C" />
    </template>
    <!-- <rect :x="x - xoffset" :y="y - yoffset" :width="30" :height="13" fill="white" /> -->
    <text :x="cx + xoffset" :y="cy + yoffset + textoffset" :text-anchor="textanchor" font-size="10" fill="#F56C6C" font-weight="bold">{{ formatLevel(level) }}</text>
  </g>
</template>

<script>
export default {
  props: ['x', 'y', 'anchor', 'direction', 'level', 'pressure'],
  computed: {
    textanchor() {
      return {
        'ne': 'start',
        'nw': 'end',
        'se': 'start',
        'sw': 'end'
      }[this.direction]
    },
    cx() {
      return {
        'left': this.x - 12,
        'right': this.x + 12,
        'top': this.x,
        'bottom': this.x
      }[this.anchor]
    },
    cy() {
      return {
        'left': this.y,
        'right': this.y,
        'top': this.y-5,
        'bottom': this.y + 12
      }[this.anchor]
    },
    textoffset() {
      return {
        'ne': -4,
        'nw': -4,
        'se': 10,
        'sw': 10
      }[this.direction]
    },
    xoffset() {
      return {
        'ne': 5,
        'nw': -5,
        'se': 5,
        'sw': -5
      }[this.direction] + (this.pressure ? 0 : 10)
    },
    yoffset() {
      return {
        'ne': -8,
        'nw': -8,
        'se': 8,
        'sw': 8
      }[this.direction]
    },
    linewidth() {
      return {
        'ne': -25,
        'nw': 25,
        'se': -25,
        'sw': 25
      }[this.direction]
    },
    level_line() {


      let line = `M ${this.cx} ${this.cy} L ${this.cx + this.xoffset} ${this.cy + this.yoffset} L ${this.cx + this.xoffset - this.linewidth} ${this.cy + this.yoffset}`
      return line
    },
    level_triangle() {
      let x = this.x
      let y = this.y - 2
      let width = 9
      let height = 7
      let offset = -30
      let path = `M ${x} ${y}
                  L ${x - width/2} ${y - height}
                  L ${x + width/2} ${y - height}
                  Z
                  M ${x} ${y - height}
                  L ${x-offset} ${y - height}`
      return path
    },
    path() {

      let path = ''

      // draw a triangle
      if (this.direction == 'left') {
        let x = this.x - 16
        let y = this.y - this.height - 2
        let width = 10
        let height = 10
        path = `M ${x} ${y}
                  L ${x + width} ${y}
                  L ${x + width/2} ${y + height}
                  Z
                  L ${x-28} ${y}`
      } else {
        let x = this.x - 12
        let y = this.y + 15
        let width = 10
        let height = 10
        path = `M ${x} ${y}
                  L ${x + width} ${y + height/2}
                  L ${x} ${y + height}
                  Z
                  M ${x} ${y + height/2}
                  L ${x-20} ${y + height/2}`
      }
      return path

    },
  },
  methods: {
    formatLevel(level) {
      return level.toFixed(1) + ' m'
    }
  }
}
</script>
