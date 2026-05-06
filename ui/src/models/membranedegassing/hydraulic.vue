<template>
<svg>
    <path :d="cartridge" fill="white" stroke="black" stroke-width="2" />
    <path :d="connectorBooster" fill="none" stroke="#409EFF" stroke-width="2" />
    <path v-if="this.params.num_stages ==='double'" :d="connectorStages" fill="none" stroke="#409EFF" stroke-width="2" />
   </svg>
   
   
   </template>
   
   
   <script>
   import hydraulicLine from '@/mixins/hydraulicline'

   export default {
     name: 'hydraulic-membranedegassing',    
     mixins: [hydraulicLine],     
     data() {
      return {
        r: 18
      }
    },
     computed: {
      dimensions() {
        return {
          top: this.params.inlet_elevation+2,
          bottom: this.params.inlet_elevation 
        }
      },
      anchorpoints() {
        return {
          in: { x: this.x0, y: this.y(this.params.inlet_elevation), anchor:  'left' },
          out: { x: this.params.num_stages === 'single' ? this.x0 + 0.575*this.width : this.x0 + 0.775*this.width, y: this.y(this.params.inlet_elevation+1.30), anchor: 'top'}
        }
      },
    cartridge(){

      if (this.params.num_stages === 'single') {
      var xFirst = this.x0+0.5*this.width
      var yFirst = this.y(this.params.inlet_elevation)-0.2*this.stepY
      }
      else{
        var xFirst = this.x0+0.1*this.width
        var yFirst = this.y(this.params.inlet_elevation)-0.2*this.stepY
      }
      var path = `M ${xFirst} ${yFirst}
                  H ${xFirst-0.05*this.width}
                  V ${yFirst-0.1*this.stepY}
                  H ${xFirst-0.1*this.width}
                  V ${yFirst-0.2*this.stepY}
                  H ${xFirst-0.05*this.width}
                  V ${yFirst-1*this.stepY}
                  H ${xFirst}
                  V ${yFirst-1.1*this.stepY}
                  H ${xFirst+0.15*this.width}
                  V ${yFirst-1*this.stepY}
                  H ${xFirst+0.2*this.width}
                  V ${yFirst-0.90*this.stepY}
                  H ${xFirst+0.25*this.width}
                  V ${yFirst-0.80*this.stepY}
                  H ${xFirst+0.2*this.width}
                  V ${yFirst}
                  H ${xFirst+0.15*this.width}
                  V ${yFirst+0.1*this.stepY}
                  H ${xFirst}
                  Z`
      if ( this.params.num_stages === 'double') {
      xFirst = this.x0+0.7*this.width
      yFirst = this.y(this.params.inlet_elevation)-0.2*this.stepY

      path += `M ${xFirst} ${yFirst}
                  H ${xFirst-0.05*this.width}
                  V ${yFirst-0.1*this.stepY}
                  H ${xFirst-0.1*this.width}
                  V ${yFirst-0.2*this.stepY}
                  H ${xFirst-0.05*this.width}
                  V ${yFirst-1*this.stepY}
                  H ${xFirst}
                  V ${yFirst-1.1*this.stepY}
                  H ${xFirst+0.15*this.width}
                  V ${yFirst-1*this.stepY}
                  H ${xFirst+0.2*this.width}
                  V ${yFirst-0.90*this.stepY}
                  H ${xFirst+0.25*this.width}
                  V ${yFirst-0.80*this.stepY}
                  H ${xFirst+0.2*this.width}
                  V ${yFirst}
                  H ${xFirst+0.15*this.width}
                  V ${yFirst+0.1*this.stepY}
                  H ${xFirst}
                  Z`
      }
      return path
    },
    connectorBooster(){
      if (this.params.num_stages === 'single') {
      var connect = `M ${this.x0} ${this.y(this.params.inlet_elevation)}
                  H ${this.x0+0.575*this.width}
                  V ${this.y(this.params.inlet_elevation)-0.1*this.stepY}
                  `
      }
      else{
        var connect = `M ${this.x0} ${this.y(this.params.inlet_elevation)}
                  H ${this.x0+0.175*this.width}
                  V ${this.y(this.params.inlet_elevation)-0.1*this.stepY}
                  `
      }
      return connect
    },
    connectorStages(){
      let x = this.x0+0.1*this.width
      let y = this.y(this.params.inlet_elevation)-0.2*this.stepY

      let path = `M ${x+0.075*this.width} ${y-1.11*this.stepY}
                  V ${y-1.30*this.stepY}
                  H ${x+0.3*this.width}
                  V ${y+0.2*this.stepY}
                  H ${x+0.675*this.width}
                  V ${y+0.1*this.stepY}
                  `
      return path
    },
    }, 
     methods:{
   
     }
    }


    
    </script>