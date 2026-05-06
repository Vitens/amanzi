<template>
    <svg>

        <path :d="dosingBlock" fill="white" stroke="black" stroke-width="2" />

        <text :x="this.x0+0.5*this.width" :y="this.y(this.inlet_elevation+0.6)" text-anchor="middle" font-size="12" fill="black">{{ label }}</text>
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
          top: this.inlet_elevation,
          bottom: this.inlet_elevation,
        }
      },
      inlet_elevation(){
        
        let elevation = this.params.position == 'effluent' ? this.elevation(this.upstream_elevation) : this.elevation(this.downstream_elevation)
        
        // if elevation is NaN, return 0
        if (isNaN(elevation)) { return 0 }
        return elevation

      },
      anchorpoints() {
        return {
          in: { x: this.x0+0.375*this.width, y: this.y(this.inlet_elevation), anchor:  'left' },
          out: { x: this.x0+0.625*this.width, y: this.y(this.inlet_elevation), anchor: 'right'}
        }
      },
      dosingBlock(){
        let x = this.x0 + 0.25*this.width
        let y = this.y(this.inlet_elevation)

        // triangle shape
        return `
        M ${x},${y}
        L ${x+0.25*this.width},${y+10}
        L ${x+0.50*this.width},${y}
        L ${x+0.25*this.width},${y-10}
        L ${x},${y}
        `
      },
      arrow(){

        return `
                M ${this.x0+0.35*this.width},${this.y(this.inlet_elevation+0.22)-8}
                L ${this.x0+0.5*this.width},${this.y(this.inlet_elevation+0.22)}
                L ${this.x0+0.65*this.width},${this.y(this.inlet_elevation+0.22)-8}
                M ${this.x0+0.5*this.width},${this.y(this.inlet_elevation+0.22)}
                L ${this.x0+0.5*this.width},${this.y(this.inlet_elevation+0.22)-20}
                `
      },
        label(){
            return this.params.chemical
        },
        labelbox(){
            let x = this.x0+0.375*this.width
            let y = this.y(this.inlet_elevation)
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
