<template>
    <svg>
    
      <path :d="membraneUnit" fill="white" stroke="black" stroke-width="2"  />
    
    </svg>
    
    
    </template>
    
    
    <script>
    import hydraulicLine from '@/mixins/hydraulicline'

    export default {
      name: 'hydraulic-membrane',    
      
      mixins: [hydraulicLine], 
      data() {
        return {
          r: 15
        }
      },

     computed: {
      elevation() {
        return this.params.inlet_elevation
      },
      dimensions() {
        return {
          top: this.params.inlet_elevation+this.params.number_of_stages+0.5,
          bottom: this.params.inlet_elevation 
        }
      },
      anchorpoints() {
        return {
          in: { x: this.x0+0.1*this.width, y: this.y(this.params.inlet_elevation), anchor:  'left' },
          out: { x: this.x0 + 0.9*this.width, y: this.y(this.params.inlet_elevation)-(this.params.number_of_stages-1)*(0.5*this.stepY+10), anchor: 'right'}
        }
      },  
      membraneUnit(){
        var x = this.x0+0.1*this.width
        var y = this.y(this.params.inlet_elevation)
        var width = 0.8*this.width
        var height = 0.5*this.stepY
        var path = ``
         for (let i = 0; i < this.params.number_of_stages; i++) {
          path += this.rect(x, y+0.5*height-i*(height+10), width, height)
          path += `M ${x} ${y+0.5*height-i*(height+10)} L ${x+width} ${y+0.5*height-i*(height+10)-height}`
         }
         return path
      },
      boosterTriangle() {
            const cx = this.x0 + this.r;
            const cy = this.y(this.params.inlet_elevation);
            const r = this.r-2;

            const string = `${cx + r},${cy} ${cx - r/2},${cy - r * 0.866} ${cx - r/2},${cy + r * 0.866}`;
            return string
        },
      connectorBooster(){
      var connect = `M ${this.x0 + this.r} ${this.y(this.params.inlet_elevation)}
                  H ${this.x0+0.3*this.width - 2}
                  `
      return connect
    }
   
      },
      methods:{
        format(value) {
          return '+' + value.toFixed(1) + ' m'
        }

      }
      }
    
    </script>