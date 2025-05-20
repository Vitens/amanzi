<template>
    <svg>
        <path :d="filterdimensions.rect" fill="white" stroke="black" stroke-width="2"  />
        <path v-if="!this.params.spray && !this.params.pressurized" :d="inlet" fill="white" stroke="black" stroke-width="2"  />
        <path v-if="this.params.spray" :d="sprayunit" fill="none" stroke="black" stroke-width="2"  />
        <path v-if="this.params.dual_media" :d="antraLayer" fill="grey" stroke="black" stroke-width="2"/>
        <path :d="marbleLayer" fill="white" stroke="black" stroke-width="2"  />
        <path :d="supernatant" fill="none" stroke="#409EFF" stroke-width="2"  />
        <path :d="overflowFix" fill="none" stroke="white" stroke-width="3"  />
    
    </svg>
    
    
    </template>
    
    
    <script>
    import hydraulicLine from '@/mixins/hydraulicline'

    export default {
      name: 'hydraulic-marblefilter',    
      props: ['position', 'config', 'path' , 'dim'],
      mixins: [hydraulicLine],

      computed: {
      bottom() {
        return this.params.inlet_elevation-(this.params.fall_height_to_media + this.params.bed_height_start + this.params.filter_bottom + (this.params.dual_media ? this.params.height_anthracite : 0))
      },
      dimensions() {
        return {
          top: this.params.inlet_elevation,
          bottom: this.bottom
        }
      },
      anchorpoints() {
        let inlet_y = (this.params.spray || this.params.pressurized) ? this.y(this.params.inlet_elevation) : this.y(this.params.inlet_elevation-0.15)

        // let h_anthracite = this.params.dual_media ? this.params.height_anthracite : 0

        let outlet_y = this.y(this.params.inlet_elevation-this.params.fall_height_to_media - h_anthracite - this.params.bed_height_start - this.params.filter_bottom/2)

        return {
          in: { x: (this.params.spray || this.params.pressurized) ? this.x0+0.1*this.width : this.x0 , y: inlet_y, anchor: 'left'},
          out: { x: this.x0 + 0.9*this.width, y: outlet_y, anchor: 'right'}
        }
      },
      // antraLayer(){
      //   let anthraciteHeight = this.params.height_anthracite*this.stepY
      //   let yAntra = this.y(this.params.inlet_elevation);
      //   if (this.params.spray){
      //     yAntra = yAntra + this.params.fall_height_to_media*this.stepY;
      //     var anthraciteLayer = this.Layer(this.x0+0.1*this.width, yAntra, 0.8*this.width,anthraciteHeight);
      //   }
      //   else if(this.params.pressurized){
      //     yAntra = yAntra + this.params.fall_height_to_media*this.stepY;
      //     var anthraciteLayer = this.Layer(this.x0+0.1*this.width, yAntra, 0.8*this.width,anthraciteHeight);
      //   }
      //   else {
      //     yAntra = yAntra + this.params.fall_height_to_media*this.stepY;
      //     var anthraciteLayer = this.Layer(this.x0+0.2*this.width, yAntra, 0.7*this.width,anthraciteHeight);
      //   }
      //   return anthraciteLayer;
      // },
      marbleLayer(){
        let marbleHeight = this.params.bed_height_start*this.stepY;
        let ymarble = this.y(this.params.inlet_elevation);
        if (this.params.dual_media){
          ymarble = ymarble + this.params.height_anthracite*this.stepY;
        }
        if (this.params.spray){
          ymarble = ymarble + this.params.fall_height_to_media*this.stepY;
          var marbleLayer = this.Layer(this.x0+0.1*this.width, ymarble, 0.8*this.width, marbleHeight);
        }
        else if(this.params.pressurized){
          ymarble = ymarble + this.params.fall_height_to_media*this.stepY;
          var marbleLayer = this.Layer(this.x0+0.1*this.width, ymarble, 0.8*this.width, marbleHeight);
        }
        else {
          ymarble = ymarble + this.params.fall_height_to_media*this.stepY;
          var marbleLayer = this.Layer(this.x0+0.2*this.width, ymarble, 0.7*this.width, marbleHeight);
        }
        return marbleLayer;
      },
      filterdimensions(){
        let distance_to_top = 0.12 // m
        var filterheight =(this.params.bed_height_start+distance_to_top+this.params.filter_bottom+this.params.fall_height_to_media)*this.stepY;

        if (this.params.dual_media){
          filterheight = filterheight + this.params.height_anthracite*this.stepY;
        }

        if (this.params.spray && !this.params.pressurized){
          var filterrect = this.filterwithoutTop(this.x0+0.1*this.width, this.y(this.params.inlet_elevation)-distance_to_top*this.stepY, 0.8*this.width, -filterheight);
        }
        else if (!this.params.spray && !this.params.pressurized){
          var filterrect = this.filterwithoutTop(this.x0+0.2*this.width, this.y(this.params.inlet_elevation)-distance_to_top*this.stepY, 0.7*this.width, -filterheight);
        }
        else if (this.params.pressurized && !this.params.spray){
          var filterrect = this.smoothEdgeRect(this.x0+0.1*this.width, this.y(this.params.inlet_elevation), 0.8*this.width, filterheight,25);
        }
        else if (this.params.pressurized && this.params.spray){
          var filterrect = this.smoothEdgeRect(this.x0+0.1*this.width, this.y(this.params.inlet_elevation), 0.8*this.width, filterheight, 25);
        }
        return {rect:filterrect};
      },
      levels() {
        let levels = [];
        if (!this.params.spray && !this.params.pressurized){
          levels.push({
            x: this.x0+0.1*this.width,
            y: this.y(this.params.inlet_elevation),
            level: this.params.inlet_elevation,
            direction: 'ne'
          })
        }
        if (!this.params.pressurized){
          levels.push({
            x: this.x0+0.3*this.width,
            y: this.y(this.params.inlet_elevation-this.params.fall_height_to_media+this.params.supernatant_level),
            level: this.params.inlet_elevation-this.params.fall_height_to_media+this.params.supernatant_level,
            direction: 'ne'
          })
        }
        return levels
      },
      sprayunit(){
        let width = this.width*0.8;
        let ySpray = this.y(this.params.inlet_elevation);
        let x = this.x0+0.1*this.width;
        var path = `M ${x } ${ySpray} H ${x + width * 0.75 } M ${x+0.25*width} ${ySpray} L ${x + width * 0.25 } ${ySpray+12} M ${x+0.25*width } ${ySpray} L ${x + width * 0.3 } ${ySpray+12} M ${x+0.25*width } ${ySpray} L ${x + width * 0.2 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.45 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.55 } ${ySpray+12} M ${x+0.5*width } ${ySpray} L ${x + width * 0.5 } ${ySpray+12}
        M ${x+0.75*width } ${ySpray} L ${x + width * 0.7 } ${ySpray+12} M ${x+0.75*width } ${ySpray} L ${x + width * 0.75 } ${ySpray+12} M ${x+0.75*width } ${ySpray} L ${x + width * 0.8 } ${ySpray+12}`;
        return path;
      },
      supernatant(){
        let yWater = this.y(this.params.inlet_elevation - this.params.fall_height_to_media + this.params.supernatant_level);
        let x = this.x0;
        if (this.params.spray){
          var path = `M ${x+0.1*this.width} ${yWater} H ${x + 0.9*this.width} `;
        }
        else if(this.params.pressurized){
          var path = `M ${x+0.1*this.width } ${yWater} H ${x + 0.9*this.width}`;
        }
        else {
          var path = `M ${x} ${this.y(this.params.inlet_elevation)} H ${x+0.2*this.width } M ${x+0.2*this.width } ${yWater} H ${x + 0.9*this.width} `;
        }
        return path;
      },
      inlet(){
        let x = this.x0;
        let yInlet = this.y(this.params.inlet_elevation)-10;
        let width = 0.2*this.width;
        let height = -0.5* this.stepY;
        let path = this.filterwithoutTop(x, yInlet, width, height);
        return path;
      },
      overflowFix(){
        let x = this.x0+0.2*this.width;
        let yInlet = this.y(this.params.inlet_elevation)-20;
        let path = `M ${x} ${yInlet}
                    V ${yInlet+19}
                    `
        return path;
      },
      boosterElevation(){
        return this.dimensions.bottom
      },
      },
      methods:{
        Layer(x, y, width, height){
          var path = `M ${x} ${y} L ${x+width} ${y} L ${x+width} ${y+height} L ${x} ${y+height} L ${x} ${y}  L ${x+width} ${y+height} M ${x} ${y+height} L ${x+width} ${y}Z`;
          return path;
        },
        filterwithoutTop(x, y, width, height){
          return `M ${x} ${y} 
                  L ${x} ${y - height} 
                  L ${x + width} ${y - height} 
                  L ${x + width} ${y} 
                  `;
        }
      }
    }
    </script>