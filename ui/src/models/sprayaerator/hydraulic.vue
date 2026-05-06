<template>
    <svg>
      <path :d="vacuum.oval" fill="none" stroke="black" stroke-width="2"  /> 
      <path :d="vacuum.spray" fill="none" stroke="black" stroke-width="2"  />
      <path :d="vacuum.valves" fill="none" stroke="black" stroke-width="2"  />
      <path :d="vacuum.bottom" fill="none" stroke="black" stroke-width="2"  />

    
    
    </svg>
    
    
    </template>
    
    
    <script>
    export default {
      name: 'hydraulic-sprayaerator',    
      props: ['position', 'config', 'path' , 'dim'],
      
      data() {
        return {
          anchorpoints: {},
          numberofmodels: this.path.length-1, //excluding the output model
          total_width: this.dim.width*0.95,
          total_height: this.dim.height,
    
    
        }
      },
      computed: {
      params() {
        return this.config.parameters
          },
      vacuum() {
        var radius = 50;
    
        var heightfactor =this.params.fall_height+this.dim.stepY*this.params.influent_pressure_loss; // heigght not correct bedheight also relevant
        var unitwidth = this.total_width/ this.numberofmodels 
        var x = (unitwidth * (this.position))+ 0.2*unitwidth  ;
        var y = this.total_height-(this.total_height-this.dim.upperOffset-((this.dim.maxY-this.params.inlet_elevation)*this.dim.stepY))-radius*0.5;
        var x2 = x+radius*2;


        var path2 = `M ${x + radius } ${y} 
                  C ${x + radius * 0.614 } ${y + 0.015 } ${x + radius * 0.302 } ${y + radius * 0.313 } ${x + radius * 0.302 } ${y + radius * 0.698 } 
                  V ${y + radius * 1.302 + heightfactor } 
                  C ${x + radius * 0.302 } ${y + radius * 1.687 + heightfactor } ${x + radius * 0.614 } ${y + radius * 2 + heightfactor } ${x + radius } ${y + radius * 2 + heightfactor } 
                  c ${radius * 0.386 } ${-0.015 } ${radius * 0.698 } ${-radius * 0.313  } ${radius * 0.698 } ${-radius * 0.698 } 
                  V ${y + radius * 0.698  } 
                  C ${x + radius * 1.698 } ${y + radius * 0.313   } ${x + radius * 1.386 } ${y + 0.015  } ${x + radius } ${y} 
                  Z`;
        var path3= `M ${x+0.3*radius } ${y+radius*0.5} H ${x + radius * 1.4 } Z`;
        // create spray
        var path4 = `M ${x+0.6*radius } ${y+radius*0.5} L ${x + radius * 0.8 } ${y+radius*0.8} M ${x+0.6*radius } ${y+radius*0.5} L ${x + radius * 0.4 } ${y+radius*0.8} M ${x+0.6*radius } ${y+radius*0.5} L ${x + radius * 0.6 } ${y+radius*0.8} M ${x+1.2*radius } ${y+radius*0.5} L ${x + radius * 1.4 } ${y+radius*0.8} M ${x+1.2*radius } ${y+radius*0.5} L ${x + radius * 1.2 } ${y+radius*0.8} M ${x+1.2*radius } ${y+radius*0.5} L ${x + radius * 1 } ${y+radius*0.8}`;

        var bottom = `M ${x + radius * 0.302 } ${y + radius * 1.302 + heightfactor} 
                    H ${x + radius * 1.698 }
                    M ${x2-(x2-x)*0.4} ${y + radius * 1.302 + heightfactor-5} 
                    L ${x2-(x2-x)*0.6} ${y + radius * 1.302 + heightfactor-5} 
                    M ${x2-(x2-x)*0.3} ${y + radius * 1.302 + heightfactor-10} 
                    L${x2-(x2-x)*0.7} ${y + radius * 1.302 + heightfactor-10}
                    M ${x2-(x2-x)*0.2} ${y + radius * 1.302 + heightfactor-15} 
                    L${x2-(x2-x)*0.8} ${y + radius * 1.302 + heightfactor-15} 
                    
                    Z`;

                  

        this.anchorpoints = { end: { x: x+0.3*radius, y: y+radius*0.5, anchor: 'left' } };
    
        this.anchorpoints.start = { x: x+ 2*radius-0.3*radius, y: y+radius*1.4+heightfactor, anchor: 'right' };
        
      
        this.emitAnchorpoints();
      
        return {oval:path2, spray: path3 , valves:path4, bottom: bottom};  
    }
      },
      methods:{
       emitAnchorpoints() {
          // console.log('emitting anchor points')
          const data = this.anchorpoints;
          this.$emit('anchor', data , this.position);
          },
      }
      }
    
    </script>