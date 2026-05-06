<template>
    <svg>
        <path :d="tank" fill="white" stroke="black" stroke-width="2"  />
        <path :d="filling" fill="white" stroke="black" stroke-width="2"  />
        <path :d="sprayunit" fill="white" stroke="black" stroke-width="2"  />
    
    </svg>
    
    
    </template>
    
    <script>
    import hydraulicLine from '@/mixins/hydraulicline'

    export default {
      name: 'hydraulic-toweraeration',    
      mixins: [hydraulicLine],

      computed: {
      anchorpoints() {
      return {
        in: { x: this.x0+0.1*this.width, y: this.y(this.params.inlet_elevation), anchor: 'left' },
        out: { x: this.x0 + 0.90 * this.width-1, y: this.y(this.params.inlet_elevation)+this.stepY*(this.params.bed_height+this.params.fall_height+0.5), anchor: 'right' }
      }
    },
    boosterElevation() {
      return this.params.inlet_elevation - this.params.bed_height-this.params.fall_height-1
    },
      dimensions() {
        return {
          bottom: this.params.inlet_elevation - (this.params.bed_height+this.params.fall_height+1),
          top: this.params.inlet_elevation +1 
        }
      },

      tank() {
        let width = this.width*0.8;
        let x = this.x0+0.1*width;
        let y= this.y(this.params.inlet_elevation);
        let path = `M ${x} ${y} 
                    V ${y + this.stepY*(this.params.bed_height+this.params.fall_height+1.0)} 
                    H ${x + width} 
                    V ${y - 0.5*this.stepY}
                    H ${x + 0.8*width}
                    V ${y - 1*this.stepY}
                    H ${x + 0.2*width}
                    V ${y - 0.5*this.stepY}
                    H ${x}
                    Z
             `;
        return path;
      },
      filling() {
        let width = this.width*0.8;
        return this.Layer(this.x0+0.1*width, this.y(this.params.inlet_elevation)+this.params.fall_height*this.stepY, width, this.stepY*(this.params.bed_height));
      },
      sprayunit(){
        let width = this.width*0.8;
        let ySpray = this.y(this.params.inlet_elevation);
        let x = this.x0+0.1*width;
        var path = `M ${x } ${ySpray} H ${x + width * 0.75 } M ${x+0.25*width} ${ySpray} L ${x + width * 0.25 } ${ySpray+12} M ${x+0.25*width } ${ySpray} L ${x + width * 0.3 } ${ySpray+12} M ${x+0.25*width } ${ySpray} L ${x + width * 0.2 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.45 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.55 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.5 } ${ySpray+12}
        M ${x+0.75*width } ${ySpray} L ${x + width * 0.7 } ${ySpray+12} M ${x+0.75*width } ${ySpray} L ${x + width * 0.75 } ${ySpray+12} M ${x+0.75*width } ${ySpray} L ${x + width * 0.8 } ${ySpray+12}`;
        return path;
      },

    //   tower() {
    //   var radius = 50;
    
    //   var heightfactor =this.dim.stepY*(this.params.influent_pressure_loss+this.params.bed_height+this.params.fall_height+this.params.pressure_loss_nozzles); 
    //   var graphheight = heightfactor/(heightfactor + radius*2*0.3);
    //   var unitwidth = this.total_width/ this.numberofmodels 
    //   var x = (unitwidth * (this.position))+ 0.2*unitwidth  ;
    //   var y = this.total_height-(this.total_height-this.dim.upperOffset-((this.dim.maxY-this.params.inlet_elevation)*this.dim.stepY))-radius*0.5;


    //   var path2 = `M ${x + radius } ${y} 
    //              C ${x + radius * 0.75} ${y} ${x + radius * 0.25} ${y + radius * 0.25} ${x + radius * 0.25} ${y + radius * 0.75} 
    //             V ${y + radius * 0.5 + heightfactor * graphheight} 
    //             C ${x + radius * 0.25} ${y + radius * 1.25 + heightfactor * graphheight} ${x + radius * 0.75} ${y + radius * 1.5 + heightfactor * graphheight} ${x + radius} ${y + radius * 1.5 + heightfactor * graphheight} 
    //             c ${radius * 0.25} ${0} ${radius * 0.75} ${-radius * 0.25} ${radius * 0.75} ${-radius * 0.75} 
    //             V ${y + radius * 0.75} 
    //             C ${x + radius * 1.75} ${y + radius * 0.25} ${x + radius * 1.25} ${y} ${x + radius} ${y} 
    //             Z`;
    //   var rect = {x: x+ radius * 0.25, y: y + radius * 0.5+0.1*heightfactor* graphheight, width: 2*radius * (1-0.25) , height:heightfactor* graphheight};
    //   var path3 = `M ${rect.x} ${rect.y} L ${rect.x+rect.width} ${rect.y+heightfactor* graphheight} M ${rect.x} ${rect.y+heightfactor* graphheight} L ${rect.x+rect.width} ${rect.y}`;
     
      
    //   return {oval:path2, rect:rect , cross: path3};  ;
    // }
      },
      methods:{

      }
    }
    
    </script>