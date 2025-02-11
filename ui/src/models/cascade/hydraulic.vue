<template>
    <svg>
      <path v-for="step in steps[0]" :d="step" stroke="black" stroke-width="2" fill="white"/>
      <path v-for="waterline in steps[1]" :d="waterline" stroke="#409EFF" stroke-width="2" fill="transparent"/>
    </svg>

  </template>
  <script>
  import hydraulicLine from '@/mixins/hydraulicline'

  export default {
    name: 'hydraulic-cascade',
    props: ['position', 'config', 'path' , 'dim'],

    mixins: [hydraulicLine],

    computed: {
      levels() {
        let levels = []
        for (let s = 0; s < this.params.number_of_steps + 1; s++) {
          levels.push({
            x: this.x0 + this.stepWidth/2 + s * this.stepWidth,
            y: this.y(this.params.inlet_elevation - s * this.params.step_height),
            level: this.params.inlet_elevation - s * this.params.step_height,
            direction: 'ne'
          })
        }
        return levels
      },
      boosterElevation() {
        return this.bottom - 0.5
      },
      dimensions() {
        return {
          top: this.params.inlet_elevation,
          bottom: this.params.inlet_elevation - (this.params.number_of_steps+1) * this.params.step_height
        }
      },
      stepWidth() {
        return this.width / (this.params.number_of_steps + 1)
      },
      stepHeight() {
        return this.length(this.params.step_height)
      },
      bottom() {
        return this.params.inlet_elevation - (this.params.number_of_steps+1) * this.params.step_height
      },
      anchorpoints() {
        return {
          in: { x: this.x0 + this.stepWidth/2, y: this.y(this.params.inlet_elevation)+this.stepHeight, anchor: 'bottom' },
          out: { x: this.x0 + this.width, y: this.y(this.bottom) - this.stepHeight/2, anchor: 'right', booster: this.bottom + 0.5 }
        }
      },
      steps() {

        let steps = []
        let waterlines = []

        let number_of_steps = this.params.number_of_steps + 1
        let step_height = this.length(this.params.step_height)

        let x = this.x0
        let y = this.y(this.params.inlet_elevation)
        let step_width = this.width / number_of_steps

        for (let s = 0; s < number_of_steps; s++) {

          // make step
          steps.push(
            `M ${x} ${y-10}
             L ${x} ${y+step_height}
             L ${x+step_width} ${y+step_height}
             L ${x+step_width} ${y-2}
             `
          )


          waterlines.push(
            this.line(x+1, y, x+step_width-1, y) + '\n' +
            this.waterline(x + step_width/2, y, 40, 3, 5)
          )

          x += step_width
          y += step_height
        }


        return [steps, waterlines]
      }
    }
  }
  </script>
  