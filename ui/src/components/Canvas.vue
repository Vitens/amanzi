<template>
<div id="viewport" ref="viewport">
  <div id='canvas' 
    @mousedown="deselect" 
    @mousemove="debug"

    @keyup.delete="deleteKey" 

    @keydown.up.prevent="$project.scenario.moveSelection(0,-5)"
    @keydown.down.prevent="$project.scenario.moveSelection(0,5)"
    @keydown.left.prevent="$project.scenario.moveSelection(-5,0)"
    @keydown.right.prevent="$project.scenario.moveSelection(5,0)"

    @keydown.shift.up.prevent="$project.scenario.moveSelection(0,-50)"
    @keydown.shift.down.prevent="$project.scenario.moveSelection(0,50)"
    @keydown.shift.left.prevent="$project.scenario.moveSelection(-50,0)"
    @keydown.shift.right.prevent="$project.scenario.moveSelection(50,0)"

    @keydown.meta.s.prevent="$project.save"
    @keydown.ctrl.s.prevent="$project.save"

    @keydown.meta.z.prevent="$project.$undo"
    @keydown.meta.y.prevent="$project.$redo"
    @keydown.ctrl.z.prevent="$project.$undo"
    @keydown.ctrl.y.prevent="$project.$redo"

    @keydown.meta.a.prevent="$project.scenario.selectAll()"
    @keydown.ctrl.a.prevent="$project.scenario.selectAll()"

    @keydown.meta.c.prevent="$project.scenario.copy()"
    @keydown.ctrl.c.prevent="$project.scenario.copy()"

    @keydown.meta.v.prevent="$project.scenario.paste()"
    @keydown.ctrl.v.prevent="$project.scenario.paste()"

    @keydown.meta.x.prevent="$project.scenario.copy(true)"
    @keydown.ctrl.x.prevent="$project.scenario.copy(true)"

    @keydown.meta.d.prevent="$project.scenario.duplicate()"
    @keydown.ctrl.d.prevent="$project.scenario.duplicate()"

    @keydown.meta.187.prevent="setZoom(display.zoom + 0.1)"
    @keydown.meta.Minus.prevent="setZoom(display.zoom - 0.1)"

    tabindex=-1
    :style="{transform: 'translate('+display.zoomX+'px,'+display.zoomY+'px)scale('+display.zoom+')translate('+(-display.zoomX)+'px,'+(-display.zoomY)+'px)', left: display.left + 'px', top: display.top + 'px', 'transform-origin': 'left top'}"
    v-draggable="{start: startPanSelect, move: panSelect, end: endPanSelect, focus: true}"
    :class="{gridlines: display.grid, panning: panning}"
    v-zoomable="{zoom, pan: panTrackpad}"
    @dragover='allowDrop'
    @drop='dropBlock'
    
    ref="canvas"
  >
    <div class="selection" :style="{
      top: Math.min(selection.start.y,selection.end.y) + 'px',
      left: Math.min(selection.start.x,selection.end.x) + 'px',
      width: Math.abs(selection.end.x - selection.start.x) + 'px',
      height: Math.abs(selection.end.y - selection.start.y) + 'px'
    }" :class="{active: selection.active}">
    </div>

    <block 
      v-for="b in $project.scenario.models" :key="b.uid"
      :info="b" 
      @sized="blockSized"
    ></block>

    <connections :positions="positions" :display="display"></connections>
  </div>
</div>
</template>

<script>
import Block from './Block.vue'
import Connections from './Connections.vue'
import draggable from '../directives/draggable.js'
import zoomable from '../directives/zoomable.js'

export default {
  name: 'Canvas',
  components: {
    Block,
    Connections
  },
  directives: {draggable, zoomable},
  data() { return {
    selection: {
      active: false,
      start: {x:0, y:0},
      end: {x:0, y:0}
    },
    validDrop: false,
    panning: false,
    sizes: {},
  }},
  mounted() {
    // subscribe to dragstart Event
    this.$bus.on('dragStart', () => { this.validDrop = true })
    this.$bus.on('setZoom', (z) => { this.setZoom(z) })
    this.$bus.on('zoomFit', (z) => { this.zoomFit() })
  },

  computed: {
    center() {
      // Initialize the return coordinates as 0
      let x = 0;
      let y = 0;

      // Ensure the required elements exist
      if (this.$refs['canvas'] && this.$refs['viewport']) {
        // Get viewport dimensions
        const viewportBounds = this.$refs['viewport'].getBoundingClientRect();
        const viewportWidth = viewportBounds.width;
        const viewportHeight = viewportBounds.height;

        // Get the zoom level
        const zoom = this.display.zoom;

        // Calculate the center coordinates
        x = (-this.display.left + (viewportWidth / 2)) / zoom;
        y = (-this.display.top + (viewportHeight / 2)) / zoom;
      }
      // Return the coordinates
      return { x, y };
    },
    positions() {
      let ret = {}
      for(var m of this.$project.scenario.models) {
        ret[m.uid] = {
          x: m.position.x,
          y: m.position.y,
          width: this.sizes[m.uid] ? this.sizes[m.uid].width : undefined,
          height: this.sizes[m.uid] ? this.sizes[m.uid].height : undefined
        }
      }
      return ret
    },

    display() {
      return this.$interface.canvas
    }
  },
  methods: {
    allowDrop(evt) {
      if(this.validDrop) {
        evt.preventDefault()
        return
      }
      return false
    },
    deselect(evt) {
      // dont deselect if middle mouse button
      if(evt.which != 2) {
        this.$project.scenario.deselectConnections()
        this.$project.scenario.deselectBlocks()
      }
    },
    dropBlock(evt) {
      let type = evt.dataTransfer.getData("text/plain") 
      var offset = this.eventToModelCoordinates(evt)
      // correct for smaller dragged object
      // align to grid
      offset.x = offset.x - 50 - offset.x % 5
      offset.y = offset.y - 50 - offset.y % 5

      let name = this.$t('models.'+type+'.name')

      this.$project.scenario.addModel(this.modelspec, this.$project.modelParameters[type], type, name, offset, evt.shiftKey)
      this.validDrop = false
    },
    eventToModelCoordinates(evt){
      const bounds = this.$refs['canvas'].getBoundingClientRect(),
        offsetX = evt.clientX - bounds.left, // evt.offsetX/Y doesn't always work
        offsetY = evt.clientY - bounds.top
      return {
        x: offsetX / this.display.zoom,
        y: offsetY / this.display.zoom
      }
    },
    selectInsideBox(append=false) {
      // if append is true, add to selection, otherwise replace selection
      this.$project.scenario.deselectBlocks()

       // define `start` and `end` points of the box
      const start = {
        x: Math.min(this.selection.start.x, this.selection.end.x),
        y: Math.min(this.selection.start.y, this.selection.end.y)
      };
      const end = {
        x: Math.max(this.selection.start.x, this.selection.end.x),
        y: Math.max(this.selection.start.y, this.selection.end.y),
      };

      for(let block of this.$project.scenario.models) {
        const size = this.sizes[block.uid] // {width, height}

        const x = block.position.x
        const y = block.position.y
        const w = size.width
        const h = size.height

        if (x + w >= start.x && x <= end.x && y + h >= start.y && y <= end.y) {
          this.$project.scenario.selectBlock(block.uid, true); // select the block if it is inside the box
        }
      }
    },
    panTrackpad(dx,dy, args, evt) {
      this.display.left -= dx 
      this.display.top -= dy
    },
    startPanSelect(x,y, args,evt) {
      // only pan when middle mouse button is clicked
      if(evt.which == 2 || this.$interface.mouseMode == 'pan') {
        this.panning = true
      } else {
        this.selection.active = true
        this.selection.start = this.eventToModelCoordinates(evt)
        this.selection.end = this.eventToModelCoordinates(evt)
      }
      return true
    },
    panSelect(dx,dy, args, evt) {
      if(this.panning) {
        this.display.left += dx 
        this.display.top += dy
      } else {

        this.selection.end = this.eventToModelCoordinates(evt)

        this.selectInsideBox(evt.shiftKey)
      }
    },
    endPanSelect() {
      this.panning = false
      this.selection.active = false
      this.$bus.emit("selection-changed")
    },
    
    zoom(dz, x, y){

      var nz = this.display.zoom + dz

      if(nz < 0.25) { dz = 0.25 - this.display.zoom; nz = 0.25 }
      if(nz > 2.0) { dz = 2.0 - this.display.zoom; nz = 2.0 }

      let z = this.display.zoom

      let offsetx = x * dz
      let offsety = y * dz

      this.display.zoom = nz

      this.display.left -= offsetx
      this.display.top -= offsety
    },

    setZoom(zoom) {
      let dz = zoom - this.display.zoom
      this.zoom(dz, this.center.x, this.center.y)
    },

    zoomFit() {

      // get all canvas objects
      let canvas = document.getElementById('canvas')
      let blocks = canvas.querySelectorAll('.model')
      // stop if no blocks
      if(blocks.length == 0) { return }

      let connections = canvas.querySelectorAll('.connection-container')
      // merge blocks and connections
      let all = [...blocks, ...connections]

      let s = this.$interface.canvas.zoom

      // get position on canvas
      let positions = all.map(el => {
        let rect = el.getBoundingClientRect()
        return {
          x: (rect.left - canvas.getBoundingClientRect().left) / s,
          y: (rect.top - canvas.getBoundingClientRect().top) / s,
          width: (rect.width) / s,
          height: (rect.height) / s
        }
      })

      let margin = 50
      // get max left, right, top, bottom
      let left = Math.min(...positions.map(p => p.x)) - margin
      let right = Math.max(...positions.map(p => p.x + p.width)) + margin
      let top = Math.min(...positions.map(p => p.y)) - margin
      let bottom = Math.max(...positions.map(p => p.y + p.height)) + margin
      
      // width and height
      let w = right - left
      let h = bottom - top

      // get viewport dimensions
      let vp = document.getElementById('viewport').getBoundingClientRect()
      let vw = vp.width
      let vh = vp.height

      // calculate zoom
      let z = Math.min(vw / w, vh / h)
      z = Math.min(1.5, Math.max(0.25, z))

      // center
      let offsetx = (vw - w * z) / 2
      let offsety = (vh - h * z) / 2
      

      // apply zoom and offset
      this.$interface.canvas.zoom = z
      this.$interface.canvas.left = -left * z + offsetx
      this.$interface.canvas.top = -top * z + offsety





    },

    deleteKey(evt) {
      evt.preventDefault();
      this.$bus.emit("delete-key")
      this.$project.scenario.deleteSelected()
    },

    blockSized(uid, width, height) {
      this.sizes[uid] = {width: width, height: height}
    }
  }

}
</script>

<style>
#viewport {
  position: absolute;
  top: 0px;
  bottom: 0px;
  left: 0px;
  outline: 1px solid blue;
  right: 0px;
  overflow: hidden;
}
#canvas :focus {
  outline: none;
}

#canvas {
  position: absolute;
  outline: 1px solid red;
  width: 10000px;
  height: 10000px;
}
#canvas.gridlines {
  background-image: linear-gradient(to right, #DDD, 1px, transparent 1px),
                    linear-gradient(to bottom, #DDD 1px, transparent 1px),
                    linear-gradient(to right, #EEE 1px, transparent 1px),
                    linear-gradient(to bottom, #EEE 1px, transparent 1px);
  background-size: 200px 200px, 200px 200px, 25px 25px, 25px 25px;
  background-position: -1px -1px, -1px -1px, -1px -1px, -1px -1px;
}

.selection {
  position: absolute;
  /* light blue border and background color */
  border: 1px dashed #00BFFF;
  background-color: rgba(0, 191, 255, 0.2);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}
.selection.active {
  opacity: 1;
}

#canvas.panning {
  cursor: grabbing;
}
</style>