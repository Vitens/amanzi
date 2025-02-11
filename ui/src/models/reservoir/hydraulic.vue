<template>
    <svg>
        <path :d=reservoirTank fill="white" stroke="black" stroke-width="2"  />
        <path :d=waterlevel fill="white" stroke="#409EFF" stroke-width="2"  />
        <path :d=inletWeir[0] fill="transparent" stroke="black" stroke-width="2"  />
        <path :d=inletWeir[1] fill="white" stroke="black" stroke-width="2"  />
        <path :d=inletWeir[2] fill="white" stroke="#409EFF" stroke-width="2"  />
    </svg>
    
    
    </template>
    
    
    <script>
    import hydraulicLine from '@/mixins/hydraulicline'

    export default {
      name: 'hydraulic-reservoir',    
      props: ['position', 'config', 'path' , 'dim'],
      mixins: [hydraulicLine],
      
      computed: {
        anchorpoints() {
          return {
            in: { x: this.x0, y: this.y(this.params.inlet_elevation-0.5), anchor: 'left' },
            out: { x: this.x0 + this.width, y: this.y(this.params.inlet_elevation - this.params.reservoir_height-0.25), anchor: 'right' }
          }
        },
        dimensions() {
          return {
            bottom: this.params.inlet_elevation-this.params.reservoir_height,
            top: this.params.inlet_elevation+1
          }
        },
        levels() {
          let waterlevel = this.params.reservoir_height - this.params.mean_water_level
          return [{
            x: this.x0 + this.width/2,
            y: this.y(this.params.inlet_elevation - waterlevel),
            level: this.params.inlet_elevation - waterlevel,
            direction: 'ne'
          }, {
            x: this.x0 + this.width/3.3,
            y: this.y(this.params.inlet_elevation),
            level: this.params.inlet_elevation,
            direction: 'ne'
          }]
        },

        waterlevel(){
          var x = this.x0;
          var y = this.y(this.params.inlet_elevation);
          var width = this.width;
          var x2 = x+width;
          var waterlvl = Math.max(0, (this.params.reservoir_height-this.params.mean_water_level)*this.stepY);
          var path =    `M${x} ${y+waterlvl} 
                          L${x+width} ${y+waterlvl} 
                          M ${x2-(x2-x)*0.45} ${y+waterlvl +10} 
                          L${x2-(x2-x)*0.55} ${y+waterlvl +10}
                          M ${x2-(x2-x)*0.6} ${y+waterlvl+5} 
                          L${x2-(x2-x)*0.4} ${y+waterlvl +5}
                          M${x+0.2*width} ${y}
                          H${x+0.4*width} 
                              `;	
            return path;
          },

        inletWeir(){
        var x = this.x0;
        var y = this.y(this.params.inlet_elevation);
        var width = this.width;
        var minDistance = 0.5*this.stepY;

        var path =    ` M${x} ${y+minDistance}
                        H${x+0.3*width} 
                        V${y+0.4*minDistance}
                        `
        var path2 =    `M${x+0.2*width} ${y}
                        L${x+0.3*width} ${y+0.4*minDistance}
                        L${x+0.4*width} ${y}
                      `;

        var path3 =    `M${x+0.2*width} ${y}
                        L${x+0.4*width} ${y}
                        `
        return [path, path2, path3];
        },
        reservoirTank(){
          var x = this.x0;
          var y = this.y(this.params.inlet_elevation);
          // var minDistance = 0.5*this.stepY;
          var minDistance = 0.5*this.stepY;
          var height_res = this.params.reservoir_height*this.stepY;
          var width = this.width;

          var filterpath = `M${x} ${y-minDistance} 
                  V${y+height_res}
                  H${x+0.7*width}
                  L${x+0.9*width} ${y+height_res+minDistance}
                  H${x+width}
                  V${y-minDistance}
                  H${x}
                  `;
          return filterpath;
        }

      },
      methods:{
      //  emitAnchorpoints() {
      //     // console.log('emitting anchor points')
      //     const data = this.anchorpoints;
      //     this.$emit('anchor', data , this.position);
      //     },
      }
      }
    
    </script>