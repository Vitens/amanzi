<template>
    <svg>
      <path :d="tank" fill="white" stroke="black" stroke-width="2"  />
      <path :d="filling" fill="none" stroke="black" stroke-width="2"  />
      <path :d="sprayunit" fill="none" stroke="black" stroke-width="2"  />
    </svg>
    
    
    </template>
    
    
    <script>
    import hydraulicLine from '@/mixins/hydraulicline'

    export default {
      name: 'hydraulic-vacuum',    
      mixins: [hydraulicLine],

      
      computed: {
        dimensions() {
        return {
          top: this.params.inlet_elevation+1,
          bottom: this.params.inlet_elevation - this.params.spray_height-this.params.bed_height-1
        }
      },
      boosterElevation() {
        return this.dimensions.bottom - 1
      },
      anchorpoints() {
        return {
          in: { x: this.x0+ 0.1*this.width , y: this.y(this.params.inlet_elevation), anchor:  'left' },
          out: { x: this.x0 + 0.5*this.width, y: this.y(this.params.inlet_elevation)+(this.params.spray_height+this.params.bed_height+0.8)*this.stepY, anchor: 'bottom'}
        }
      },
      tank() {
        return this.cylinderTank(this.x0+0.1*this.width, this.y(this.params.inlet_elevation), 0.5*(this.width*0.8), this.stepY*(this.params.bed_height+this.params.spray_height));
      },
      filling() {
        return this.Layer(this.x0+0.1*this.width, this.y(this.params.inlet_elevation)+this.params.spray_height*this.stepY, this.width*0.8, this.stepY*(this.params.bed_height));
      },
      sprayunit(){
        let width = this.width*0.8;
        let ySpray = this.y(this.params.inlet_elevation);
        let x = this.x0+0.1*this.width;
        var path = `M ${x } ${ySpray} H ${x + width * 0.75 } M ${x+0.25*width} ${ySpray} L ${x + width * 0.25 } ${ySpray+12} M ${x+0.25*width } ${ySpray} L ${x + width * 0.3 } ${ySpray+12} M ${x+0.25*width } ${ySpray} L ${x + width * 0.2 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.45 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.55 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.5 } ${ySpray+12}
        M ${x+0.75*width } ${ySpray} L ${x + width * 0.7 } ${ySpray+12} M ${x+0.75*width } ${ySpray} L ${x + width * 0.75 } ${ySpray+12} M ${x+0.75*width } ${ySpray} L ${x + width * 0.8 } ${ySpray+12}`;
        return path;
      },


      },
      methods:{
      } 
      }
    
    </script>