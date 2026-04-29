<template>
    <svg>
        <!-- <rect :x=plate.rect.x :y=plate.rect.y :width=plate.rect.width :height=plate.rect.height fill="transparent" stroke="black" stroke-width="2"/>
        <path :d=plate.path fill="none" stroke="black" stroke-width="2"  /> -->
        <path :d="plateBody" fill="white" stroke="black" stroke-width="2"  />
        <path :d="aerationplate" fill="white" stroke="black" stroke-width="2"  />
        <path :d="waterlines" fill="none" stroke="#409EFF" stroke-width="2"  />
    
    
    </svg>
    
    
    </template>
    
    
    <script>
    import hydraulicLine from '@/mixins/hydraulicline'

    export default {
      name: 'hydraulic-plate',    
      mixins: [hydraulicLine],
      
      computed: {
      anchorpoints() {
      return {
        in: { x: this.x0, y: this.y(this.params.inlet_elevation), anchor: 'left' },
        out: { x: this.x0 + this.width, y: this.y(this.params.inlet_elevation)+0.25*this.stepY, anchor: 'right' }
      }
    },
      dimensions() {
        return {
          bottom: this.params.inlet_elevation-1,
          top: this.params.inlet_elevation
        }
      },
      plateBody(){
        let x = this.x0;
        let y = this.y(this.params.inlet_elevation);
        let width = this.width;
        var path = `M ${x} ${y-10} 
                    L ${x} ${y+1*this.stepY}  
                    L ${x+0.2*width} ${y+1*this.stepY} 
                    L ${x+0.8*width} ${y+0.5*this.stepY} 
                    L ${x+width} ${y+0.5*this.stepY} 
                    L ${x+width} ${y} 
                    M ${x+0.8*width} ${y+0.5*this.stepY}
                    L ${x+0.8*width} ${y+0.5*this.stepY}
                    `;
        return path;
      }, 
      aerationplate(){
        let x = this.x0;
        let y = this.y(this.params.inlet_elevation);
        let width = this.width;
        var path = `M ${x} ${y+0.3*this.stepY} 
                    L ${x+0.2*width} ${y+0.3*this.stepY} 
                    L ${x+0.2*width} ${y}
                    M ${x+0.2*width} ${y+0.3*this.stepY}
                    L ${x+0.25*width} ${y+0.3*this.stepY}
                    M ${x+0.3*width} ${y+0.3*this.stepY}
                    L ${x+0.35*width} ${y+0.3*this.stepY}
                    M ${x+0.4*width} ${y+0.3*this.stepY}
                    L ${x+0.45*width} ${y+0.3*this.stepY}
                    M ${x+0.5*width} ${y+0.3*this.stepY}
                    L ${x+0.55*width} ${y+0.3*this.stepY}
                    M ${x+0.6*width} ${y+0.3*this.stepY}
                    L ${x+0.65*width} ${y+0.3*this.stepY}
                    M ${x+0.7*width} ${y+0.3*this.stepY}
                    L ${x+0.75*width} ${y+0.3*this.stepY}
                    M ${x+0.8*width} ${y+0.5*this.stepY}
                    L ${x+0.8*width} ${y+0.1*this.stepY}
                    `;
        return path;
      },
      waterlines(){
        let x = this.x0;
        let y = this.y(this.params.inlet_elevation);
        let width = this.width;
        var path = `M ${x} ${y} 
                    H ${x+0.205*width}
                    M ${x+0.20*width} ${y+0.1*this.stepY}
                    H ${x+width}
                    `;
        return path;
      }



    //   plate() {
    //   var unitwidth = this.total_width/ this.numberofmodels 
    //   var x = (unitwidth * (this.position))+ 0.2*unitwidth  ;
    //   var y = this.total_height-(this.total_height-this.dim.upperOffset-((this.dim.maxY-this.params.inlet_elevation)*this.dim.stepY));
    //   var width = this.total_width/this.numberofmodels/2;
    //   var height= this.dim.stepY;

    //   var rect = {x: x, y: y, width: width, height: height};
    //   var path = `M ${x} ${y+0.8*this.dim.stepY} 
    //               L ${x+0.2*width} ${y+0.8*this.dim.stepY}  
    //               M ${x+0.3*width} ${y+0.8*this.dim.stepY} 
    //               L ${x+0.5*width} ${y+0.8*this.dim.stepY} 
    //               M ${x+0.6*width} ${y+0.8*this.dim.stepY} 
    //               L ${x+0.8*width} ${y+0.8*this.dim.stepY} 
    //               M ${x+0.9*width} ${y+0.8*this.dim.stepY} 
    //               L ${x+1*width} ${y+0.8*this.dim.stepY} 
    //               Z`;

    //   this.anchorpoints = { end: { x: x, y: y+0.5*height, anchor: 'left' } };

    
    //   this.anchorpoints.start = { x: x+width, y: y+0.5*height, anchor: 'right' };
    
    
    //   this.emitAnchorpoints();
    
    //   return {rect: rect, path: path};
    // }
      },
      methods:{
      
      }
      }
    
    </script>