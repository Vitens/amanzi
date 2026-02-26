export default {
  props: ['config', 'path', 'dim', 'offset', 'width', 'uid', 'position', 'hydraulics', 'upstream_elevation', 'downstream_elevation'],
  mounted() {
    // emit size and anchorpoints when component is mounted
    this.$emit('size', this.uid, this.dimensions)
    this.$emit('anchor', this.uid, this.anchorpoints)
    this.$emit('booster', this.uid, this.boosterElevation)
    this.$emit('levels', this.uid, this.levels)
  },
  watch: {
    // emit size and anchorpoints when dimensions or anchorpoints change
    boosterElevation(newVal) {
      this.$emit('booster', this.uid, newVal)
    },
    dimensions(newVal) {
      this.$emit('size', this.uid, newVal)
    },
    anchorpoints(newVal) {
      this.$emit('anchor', this.uid, newVal)
    },
    levels(newVal) {
      this.$emit('levels', this.uid, newVal)
    }
  },
  computed: {
    draggable() {
      return this.params.inlet_elevation !== undefined
    },
    // boilerplate levels, override in model
    levels() {
      return []
    },
    // boilerplate anchorpoints, override in model
    anchorpoints() {
      return {
        in: {x: 0, y: 0, anchor: 'right'},
        out: {x: 0, y: 0, anchor: 'bottom'}
      }
    },
    // boilerplate dimensions, override in model
    dimensions() {
      return {
        bottom: 0, top: 0
      }
    },
    width(){
      return this.width
    },
    boosterElevation() {
      return this.dimensions.bottom - 1
    },
    // get model parameters
    params() {
      return this.config.configuration.parameters
    },
    // get model x0
    x0() {
      return this.offset ? this.offset : 0
    },
    // stepY is the scale factor for the y axis
    stepY() {
      let range = this.dim.maxY - this.dim.minY 
      return (this.dim.height - this.dim.upperOffset - this.dim.lowerOffset) / range
    }

  },
  methods: {
    // get elevation from y position
    elevation(y) {
      let distance_from_top = y - this.dim.upperOffset
      return this.dim.maxY - distance_from_top / this.stepY
    },
    // get y position from elevation
    y(elevation) {
      let distance_from_top = this.dim.maxY - elevation
      let y = this.dim.upperOffset + distance_from_top * this.stepY
      // if NaN, return 0
      if (isNaN(y)) { return 0 }
      return y
    },
    // convert length to pixels
    length(length) {
      return length * this.stepY
    },

    // svg path methods
    rect(x, y, width, height) {
      return `M ${x} ${y} 
              L ${x + width} ${y} 
              L ${x + width} ${y - height} 
              L ${x} ${y - height} 
              Z`
    },
    trapezoid(x, y, width1, width2, height) {
      // width1 is the width of the bottom of the trapezoid
      // width2 is the width of the top of the trapezoid
      // height is the height of the trapezoid

      // calculate the x position of the top of the trapezoid
      let x1 = x - (width1 - width2) / 2

      return `M ${x} ${y}
              L ${x1} ${y - height}
              L ${x1 + width1} ${y - height}
              L ${x + width2} ${y}
              Z`
    },
    line(x1, y1, x2, y2) {
      return `M ${x1} ${y1}
              L ${x2} ${y2}`
    },
    triangle(cx, cy, r, rotation = 0) {
      // calculate points of triangle circumscribed in circle
      let angle = (rotation - 90) * Math.PI / 180
      // Calculate three points at 120° intervals
      let points = [0, 1, 2].map(i => ({
        x: cx + r * Math.cos(angle + i * 2*Math.PI/3),
        y: cy + r * Math.sin(angle + i * 2*Math.PI/3)
      }))
      return `M ${points[0].x} ${points[0].y}
              L ${points[1].x} ${points[1].y} 
              L ${points[2].x} ${points[2].y}
              Z`
    },
    waterline(x, y, width, steps=3, step_height=10) {
      // make water level indicator
      let x1 = x - width/2
      let x2 = x + width/2
      let path = ``

      for (let s = 0; s < steps; s++) {
        let y1 = y + s * step_height
        let y2 = y + s * step_height
        x1 += step_height
        x2 -= step_height

        path += `M ${x1} ${y1}
                L ${x2} ${y2}`
      }

      return path

    },

    cylinderTank(x, y, radius, height) {
      // Start at left side and go down
      var path = `M ${x} ${y}
                 V ${y + height}
                 C ${x } ${y+height+radius} ${x + 2*radius} ${y+height+radius} ${x + 2*radius} ${y+height}
                 V ${y}
                 C ${x + 2*radius } ${y - radius } ${x } ${y -  radius} ${x} ${y}
                 `;
      return path;
    },
    smoothEdgeRect(x, y, width, height, radius){
      var path = `M ${x} ${y}
      V ${y + height-2*radius}
      C ${x } ${y+height} ${x} ${y+height} ${x + radius} ${y+height}
      H ${x + width-radius}
      C ${x + width } ${y + height } ${x+width } ${y +height} ${x+width} ${y+height-radius}
      V ${y}
      C ${x + width } ${y-radius} ${x + width } ${y-radius} ${x+width-radius} ${y-radius}
      H ${x+radius}
      C ${x } ${y-radius} ${x } ${y -  radius} ${x} ${y}
      `;
      return path;
    },
    Layer(x, y, width, height){
      var path = `M ${x} ${y} L ${x+width} ${y} L ${x+width} ${y+height} L ${x} ${y+height} L ${x} ${y}  L ${x+width} ${y+height} M ${x} ${y+height} L ${x+width} ${y}Z`;
      return path;
    },
    membraneUnit(x,y,width,height){
      return this.rect(x,y,width,height)
    }
  }
}
