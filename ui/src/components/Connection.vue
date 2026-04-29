<template>


  <g class="connection-container" @click="selectPath">

    <rect width="10" height="10" rx="0" :x="h.x-5" :y="h.y-5" v-for="h in intersections" class="intersection" :key="h.x+h.y"></rect>

    <path
      class="connection-path-background"
      v-if="!connection.active"
      :d="pathStr"
      :stroke-width="15"
      fill="none"
    ></path>
    <path
      class="connection-path"
      ref="path"
      :class="[connection.selected ? 'selected' : '', connection.type]"
      :d="pathStr"
      :stroke-width="2"
      :marker-end="markerEnd"
      fill="none"
    ></path>


    <rect width="8" height="8" rx="0" :x="h.x" :y="h.y" v-for="h,i in handles" class="handle"
      :class="handleDirection(i)"
      v-draggable="{start: startMove, move: move, end: endMove, snap: 5, index: i}"
      :key="i"
    ></rect>

    <template v-if="booster">
    <circle :cx="boosterPoint.x" :cy="boosterPoint.y" r="7" fill="#fff" stroke-width="2" stroke="#1B78F6"></circle>
    <path :d="boosterTriangle" fill="#1B78F6"></path>
    <template v-if="showBoosterInfo">
    <rect width="43" height="18" :x="boosterInfo.x" :y="boosterInfo.y" fill="#FEA" rx="3" stroke="darkorange"></rect>
    <text :x="boosterInfo.x" :y="boosterInfo.y" dx="2" dy="14" font-size="10" class="nomouse">
      {{boosterHead}}
    </text> 
    </template>
    </template>

    <template v-if="showText">
    <rect width="40" height="20" :x="midPoint.x-20" :y="midPoint.y-10" fill="#FFF" rx="3" stroke="#333" class="connection-value"
      v-draggable="{start: startTextMove, move: textMove, end: endTextMove, snap: 5}"
    ></rect>
    <text :x="midPoint.x" :y="midPoint.y" dx="-10" dy="5" font-size="11" class="nomouse">
      {{flow}}
    </text>

    <template v-if="showLoss">

    <rect width="40" height="15" :x="midPoint.x-20" :y="midPoint.y+12" fill="#FAA" rx="3" stroke="#333" class="connection-value"></rect>

    <text :x="midPoint.x" :y="midPoint.y" dx="-16" dy="23" font-size="11" class="nomouse">
      {{loss}}
    </text>
    </template>


    </template>


  </g>
</template>

<script>

import waterpipe from '../directives/waterpipe.js'
import draggable from '../directives/draggable.js'
import roundPathCorners from '../directives/roundpathcorners.js'
import intersect from '../directives/intersect.js'

const stubLength = 10

export default {
  props: ['connection', 'positions', 'index', 'allpaths'],
  directives: {draggable},
  data() { return {
    ignoreSelect: false,
    svgPadding: 20,
    midPoint: {x:0,y:0},
    boosterPoint: {x:0,y:0},
    textOffset: 0.5,
    intersections: [],
    moved: {dx:0, dy:0},
  }},

  mounted() {
    var length = this.$refs.path.getTotalLength()
    if(this.connection.customOffset) { this.textOffset = this.connection.customOffset}
    var center = this.$refs.path.getPointAtLength(length * this.textOffset)
    this.midPoint = {x:center.x, y: center.y}

    var booster = this.$refs.path.getPointAtLength(15)
    this.boosterPoint = {x:booster.x, y: booster.y}

    this.$emit('update-path', this.cid, this.path, this.index)
    this.updateIntersections()
  },
  methods: {
    rounded(path) {
      return roundPathCorners(path, 5)
    },

    updateIntersections() {

      this.intersections = []

      for (var cid in this.allpaths) {
        if(this.allpaths[cid].index >= this.index) { continue }
        let points = intersect(this.path, this.allpaths[cid].path)

        for(var p of points) {
          this.intersections.push(p)
        }

      }

    },

    selectPath(e) {
      e.stopPropagation()
      if(this.ignoreSelect) { this.ignoreSelect = false; return }
      this.$project.scenario.selectConnection(this.index)
    },
    localize(pnt, offset) {
      return {x: pnt.x- offset, y: pnt.y - offset}
    },
    startMove(x0,y0, args) {
      if(!this.connection.selected) { return false }
      // reset moved
      this.moved = {dx:0, dy:0}
      // store state before move
      this.stateBeforeMove = _.cloneDeep(this.$project.scenario.$state)
      return true
    },
    startTextMove(x0,y0, args) {
      // set offset to 50
      this.$project.scenario.updateConnectionTextOffset(this.index, 0.5)
      // reset moved
      this.moved = {dx:0, dy:0}
      // store state before move
      this.stateBeforeMove = _.cloneDeep(this.$project.scenario.$state)
      return true
    },
    textMove(dx,dy,args,evt) {
      // update moved
      this.moved.dx += dx
      this.moved.dy += dy

      let pnt = this.$parent.translateEvt(evt)
      // find closest point along line
      let best = 1000
      var length = this.$refs.path.getTotalLength()
      var bestmatch = {}
      var bestpnt = {}


      for(var i = 0.05; i<0.95; i+=0.005) {
        var center = this.$refs.path.getPointAtLength(length * i)
        var distance = Math.sqrt(Math.pow((pnt.y - center.y), 2)+Math.pow((pnt.x - center.x),2))
        if(distance < best) {
          bestmatch = i
          bestpnt = center
          best = distance 
        }
        if(best < 2) { break }
      }
      if(best < 50) {
        this.textOffset = bestmatch
        this.midPoint = bestpnt
        this.$project.scenario.updateConnectionTextOffset(this.index, bestmatch)
      }
    },
    validateMove(index, dx, dy) {
      if(index != 0 && index != this.handles.length-1) { return true }
      let point = index == 0 ? this.src : this.tgt

      switch(point.anchor) {
        case 'right':
          return this.path[index+1].x+dx >= (point.x + stubLength)
        case 'left':
          return this.path[index+1].x+dx <= (point.x - stubLength)
        case 'top':
          return this.path[index+1].y+dy >= (point.y + stubLength)
        case 'bottom':
          return this.path[index+1].y+dy <= (point.y - stubLength)
      }
    },
    move(dx,dy,args) {
      let newPath = _.cloneDeep(this.path)
      let dir = this.handleDirection(args.index)

      if (!this.validateMove(args.index, dx,dy)) { return }

      // update moved
      this.moved.dx += dx 
      this.moved.dy += dy

      // 
      if(dir == 'ns') {
        newPath[args.index+1].y += dy
        newPath[args.index+2].y += dy
      } else {
        newPath[args.index+1].x += dx
        newPath[args.index+2].x += dx
      }

      this.$project.scenario.updateConnectionPath(this.index, newPath)

    },
    endMove() {
      // if moved, commit state to undo
      if(this.moved.dx != 0 || this.moved.dy != 0) {
        this.$project.scenario.$pushUndo(this.stateBeforeMove)
      }
    },
    endTextMove() {
      this.ignoreSelect = true
      // if moved, commit state to undo
      if(this.moved.dx != 0 || this.moved.dy != 0) {
        // fix later
        // this.$project.scenario.$pushUndo(this.stateBeforeMove)
      }
    },
    handleDirection(index) {
      let start = this.path[index+1]
      let end = this.path[index+2]
      if(Math.abs(start.x - end.x) < 15 && Math.abs(start.y - end.y) < 15) { return "hidden" }
      if(start.x != end.x) {
        return "ns"
      }
      return "ew"
    },
    getAnchor(block, anchor) {
      let model = this.positions[block]

      let width = model.width ? model.width : 0;
      let height = model.height ? model.height : 0;

      var offsetX = {'left': 0, 'right': 1, 'top': 0.5, 'bottom': 0.5}
      var offsetY = {'left': 0.5, 'right': 0.5, 'top': 0, 'bottom': 1}
      var constX = {'left': -5, 'right': 5, 'top': 0, 'bottom': 0}
      var constY = {'left': 0, 'right': 0, 'top': -5, 'bottom': 5}

      return {x: model.x + offsetX[anchor]*width + constX[anchor], y: model.y+offsetY[anchor]*height + constY[anchor], anchor: anchor}
    }

  },
  watch: {
    // update all connections with path or index
    index() { 
      this.$emit('update-path', this.cid, this.path, this.index) 
      this.$nextTick(() =>{ this.updateIntersections() })
    },
    pathStr() {
      this.$emit('update-path', this.cid, this.path, this.index)
      // update connection value midpoint
      this.$nextTick(() =>{ 
        var length = this.$refs.path.getTotalLength()
        var center = this.$refs.path.getPointAtLength(length * this.textOffset)
        this.midPoint = {x:center.x, y: center.y}
        var center = this.$refs.path.getPointAtLength(15)
        this.boosterPoint = {x:center.x, y: center.y}
        // calculate and update intersections
        this.updateIntersections()
      })

   
    }

  },

  computed: {
    loss() {
      if(!this.$runtime.solveState.connections || !this.$runtime.solveState.connections[this.cid]) { return "" }
      return "-"+this.$runtime.solveState.connections[this.cid].headloss.toFixed(1) + " m"
    },
    showBoosterInfo() {
      if(!this.$interface.display.booster_info) { return false }
      return true
    },
    showLoss() {
      if(!this.$interface.display.losses) { return false }
      if(!this.$runtime.solveState.connections || !this.$runtime.solveState.connections[this.cid]) { return false }
      if (this.$runtime.solveState.connections[this.cid].headloss == 0) { return false }
      return true
    },
    showText() {
      if(!this.$interface.display.flows) { return false }

      if(this.src.y == this.tgt.y) {
        return Math.abs(this.src.x - this.tgt.x) > 40
      }
      return true
    },
    textPoint() {
      return this.midPoint
    },
    cid() {
      return this.connection.src+" -> "+
             this.connection.tgt+" ("+this.connection.type+")"
    },
    booster() {
      if(!this.$interface.display.boosters) { return false }

      if(!this.$runtime.solveState.connections || !this.$runtime.solveState.connections[this.cid]) {
        return false
      }
      return this.$runtime.solveState.connections[this.cid].booster
    },
    boosterInfo() {
      
      let x = this.src.anchor == 'right' ? this.boosterPoint.x-15 : this.boosterPoint.x+15
      let y = this.src.anchor == 'right' ? this.boosterPoint.y-30 : this.boosterPoint.y-10

      return {x: x, y: y}
    },
    boosterHead() {
      if(!this.booster) { return "" }
      return "+" + this.$runtime.solveState.connections[this.cid].booster_head.toFixed(1) + " m"
    },
    boosterTriangle() {
      var center = this.boosterPoint
      var trianglePoints = []
      for(var i = 0; i < 3; i++) {
        var angle = Math.PI*2/3*i
        trianglePoints.push({x: center.x + Math.cos(angle)*7, y: center.y + Math.sin(angle)*7})
      }
      // generate path string
      const path = "M"+trianglePoints[0].x+","+trianglePoints[0].y+" "+
             "L"+trianglePoints[1].x+","+trianglePoints[1].y+" "+
             "L"+trianglePoints[2].x+","+trianglePoints[2].y+" "+
             "Z"

      return path
    },
    flow() {
      // if cid in state, return value
      if(!this.$runtime.solveState.connections) {
        return "!"
      }
      if(this.$runtime.solveState.connections[this.cid]) {
        return _.round(this.$runtime.solveState.connections[this.cid].flow, 2)
      } else {
        return "?"
      }
    }    ,    
    src() {
      return this.getAnchor(this.connection.src, this.connection.srcAnchor)
    },
    tgt() {
      if(this.connection.customTgt && this.connection.customTgt.x) {
        return {x: this.connection.customTgt.x, y: this.connection.customTgt.y, anchor: this.connection.tgtAnchor}
      }
      return this.getAnchor(this.connection.tgt, this.connection.tgtAnchor)
    },
    markerEnd() {
      let cls = this.connection.selected ? 'selected' : this.connection.type
      return "url(#arrow-"+cls+")"
    },

    info() {
      return waterpipe.describe(this.src, this.tgt, {stubLength: 15})
    },
    handles() {
      var ret = []
      if(!this.connection.selected) { return [] }

      for(var idx = 0; idx < this.nodes.length-1; idx += 1) {
        let x = (this.nodes[idx].x + this.nodes[idx+1].x) / 2
        let y = (this.nodes[idx].y + this.nodes[idx+1].y) / 2

        ret.push({x: x-1, y: y-1})
      }
      
      return ret
    },
    nodes() {
      var ret = []
      this.path.slice(1,-1).forEach((pnt) => {
        ret.push(this.localize(pnt, 3))
      })
      return ret
    },
    path() {
      if(this.connection.customPath && this.connection.customPath.length > 0) { return this.connection.customPath }
      let path = waterpipe.makePath(this.info)
      // splice in extra endpoints to pin start and end stubs
      path.splice(1,0,_.cloneDeep(path[1]))
      path.splice(1,0,_.cloneDeep(path[1]))
      path.splice(path.length-2,0,_.cloneDeep(path[path.length-2]))
      path.splice(path.length-2,0,_.cloneDeep(path[path.length-2]))
      return path
    },
    start() {
      return this.info.start
    },
    pathStr() {

      var ret = "M"+(this.src.x)+","+
          (this.src.y)+" "
      this.path.forEach((pnt) => {
        ret += "L"+(pnt.x)+","+
            (pnt.y)+" "
      })

      return roundPathCorners(ret, 5)

    }
  },

}
</script>

<style>
.intersection {
  fill: white;
}
.connection-container {
  position: absolute;
}
.connection-container:hover {
  cursor: pointer;
}
.connection-path {
  stroke: #444;
}
.connection-path {
  pointer-events: none;
}
.connection-path-background {
  stroke: transparent;
  cursor: pointer;
}
.connection-path-background:hover {
  stroke: #EEEEFF;
}
.connection-path.selected {
  stroke: orange !important;
}
.connection-container .node {
  fill: #fff;
  stroke: #444;
}
.connection-container .handle {
  fill: yellow;
  stroke: #444;
  z-index: 1000;
}
.connection-container .hidden {
  display: none;
}
.connection-container .handle.ns {
  cursor: ns-resize;
}
.connection-container .handle.ew {
  cursor: ew-resize;
}
.connection-container .handle:hover {
  fill: red;
}

.connection-path.waste {
  stroke: brown;
}
.connection-path.new {
  stroke: #333;
}
.connection-path.product {
  stroke: #1B78F6;
}
.connection-path.flush {
  stroke: #409EFF;
  stroke-dasharray: 8;

}
.connection-value {
  cursor: move;
}
.connection-value:hover {
  fill: #FEE;
}
.nomouse {
  pointer-events: none;
}

</style>