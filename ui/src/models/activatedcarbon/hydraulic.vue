<template>
<svg>
  <path :d="acfilter.oval" fill="none" stroke="black" stroke-width="2"  /> 
  <rect :x="acfilter.rect.x" :y="acfilter.rect.y" :width="acfilter.rect.width" :height="acfilter.rect.height" fill="white" stroke-width="2" stroke="black"/> 
  <path :d="acfilter.cross" fill="none" stroke="black" stroke-width="2"  />
</svg>


</template>


<script>
export default {
  name: 'hydraulic-activatedcarbon',    
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
  acfilter() {


    var radius = 50;
    
    var heightfactor =this.dim.stepY*(this.params.influent_pressure_loss+this.params.bed_height); 
    var graphheight = heightfactor/(heightfactor + radius*2*0.3);
    var unitwidth = this.total_width/ this.numberofmodels 
    var x = (unitwidth * (this.position))+ 0.2*unitwidth  ;
    var y = this.total_height-(this.total_height-this.dim.upperOffset-((this.dim.maxY-this.params.inlet_elevation)*this.dim.stepY))-radius*0.5;


    var path2 = `M ${x + radius } ${y} 
              C ${x + radius * 0.75} ${y} ${x + radius * 0.25} ${y + radius * 0.25} ${x + radius * 0.25} ${y + radius * 0.75} 
              V ${y + radius * 0.5 + heightfactor * graphheight} 
              C ${x + radius * 0.25} ${y + radius * 1.25 + heightfactor * graphheight} ${x + radius * 0.75} ${y + radius * 1.5 + heightfactor * graphheight} ${x + radius} ${y + radius * 1.5 + heightfactor * graphheight} 
              c ${radius * 0.25} ${0} ${radius * 0.75} ${-radius * 0.25} ${radius * 0.75} ${-radius * 0.75} 
              V ${y + radius * 0.75} 
              C ${x + radius * 1.75} ${y + radius * 0.25} ${x + radius * 1.25} ${y} ${x + radius} ${y} 
              Z`;
    var rect = {x: x+ radius * 0.25, y: y + radius * 0.5+0.1*heightfactor* graphheight, width: 2*radius * (1-0.25) , height:heightfactor* graphheight};
    var path3 = '';
    var hatchSpacing = 10;
    for (var i = -rect.height; i < rect.width; i += hatchSpacing) {
    var startX = rect.x + i;
    var startY = rect.y;
    var endX = rect.x + i + rect.height;
    var endY = rect.y + rect.height;

    // Ensure lines stay within the rectangle's boundaries
    if (startX < rect.x) {
        startY += rect.x - startX;
        startX = rect.x;
    }
    if (endX > rect.x + rect.width) {
        endY -= endX - (rect.x + rect.width);
        endX = rect.x + rect.width;
    }

    path3 += `M ${startX} ${startY} L ${endX} ${endY} `;
}
    this.anchorpoints = { end: { x: x+0.3*radius, y: y+radius*0.5, anchor: 'left' } };
 
    this.anchorpoints.start = { x: x+ 2*radius-0.3*radius, y: y+radius+heightfactor*graphheight, anchor: 'right' };
    


  this.emitAnchorpoints();

  return {oval:path2, rect:rect , cross: path3};
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