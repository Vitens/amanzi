<template>
    <svg>

        <path :d="dosingBlock" fill="white" stroke="black" stroke-width="2" />

        <text :x="this.x0+0.5*this.width" :y="this.y(this.params.inlet_elevation+0.6)" text-anchor="middle" font-size="12" fill="black">{{ label }}</text>
        <path :d="arrow" fill="none" stroke="black" stroke-width="2" />

        
  
    </svg>
  
  </template>
  <script>
     import hydraulicLine from '@/mixins/hydraulicline'


    export default {
        name: 'hydraulic-dosing',
        mixins: [hydraulicLine],     

    computed: {   
        dimensions() {
        return {
          top: this.params.inlet_elevation+1,
          bottom: this.params.inlet_elevation
        }
      },
      anchorpoints() {
        return {
          in: { x: this.x0+0.375*this.width, y: this.y(this.params.inlet_elevation), anchor:  'left' },
          out: { x: this.x0+0.625*this.width, y: this.y(this.params.inlet_elevation), anchor: 'right'}
        }
      },
      dosingBlock(){
        return  this.rect(this.x0+0.375*this.width, this.y(this.params.inlet_elevation-0.15), 0.25*this.width, this.stepY*0.3)
      },
      arrow(){

        return `
                M ${this.x0+0.47*this.width},${this.y(this.params.inlet_elevation+0.22)-12}
                L ${this.x0+0.5*this.width},${this.y(this.params.inlet_elevation+0.22)}
                L ${this.x0+0.53*this.width},${this.y(this.params.inlet_elevation+0.22)-12}
                M ${this.x0+0.5*this.width},${this.y(this.params.inlet_elevation+0.22)}
                L ${this.x0+0.5*this.width},${this.y(this.params.inlet_elevation+0.22)-20}
                `
      },
        label(){
            return this.params.chemical
        },
        labelbox(){
            let x = this.x0+0.375*this.width
            let y = this.y(this.path[this.position+1].configuration.parameters.inlet_elevation)-40
            let width = 0.25*this.width
            let height = 20
            let path = this.rect( x, y, width, height)
            path += `M ${this.x0+0.5*this.width},${y}
                     V ${y+40}`
            return path }
        },

        methods:{

        }
    }

  </script>
<style></style>
