<template>
  <div class="hydraulic-controls">
  <el-select v-model="path_index" placeholder="Select a path" style="width: 90%; margin-bottom: 5px;">
    <el-option v-for="path, idx in filteredPaths" :key="path.map(m => m.uid).join('-')"
      :label="path.map(m => m.name).join(' → ')" :value="idx">
    </el-option>
  </el-select>
  <el-checkbox v-model="showLevels" border>{{ $t('models.filtration.design.show_levels') }}</el-checkbox>
  <el-checkbox v-model="showModelLevels" border>{{ $t('models.filtration.design.show_model_levels') }}</el-checkbox>
  <el-checkbox v-model="highlightEditingModel" border>{{ $t('models.filtration.design.highlight_editing_model') }}</el-checkbox>
  </div> 

  <div class="hydraulic-container">
  
    <svg width="61" :height="graphDimensions.height" class="hydraulic-axis">
      <!-- Y-axis -->
      <line id="fixed" x1="60" :y1="graphDimensions.upperOffset" x2="60" :y2="graphDimensions.height" stroke="black"
        stroke-width="2" />
      <!-- Horizontal lines and labels -->
      <g v-for="y in yAxisValues" :key="y">
        <line :x1="55" :y1="yScale(y)" :x2="62" :y2="yScale(y)" stroke="black" />
        <text :x="50" :y="yScale(y) + 5" font-size="15" text-anchor="end">{{ y }}.0 m</text>
        <line :x1="61" :y1="yScale(y)" :x2="graphWidth" :y2="yScale(y)" stroke="#CCC" />
      </g>

    </svg>

    <div style="overflow: auto; width: 100%; height: 100%; position: relative;">
      <svg :width="graphWidth" :height="graphDimensions.height" class="hydraulic-graph">


        <!-- Horizontal lines and labels -->
        <g v-for="y in yAxisValues" :key="y">
          <line :x1="55" :y1="yScale(y)" :x2="55" :y2="yScale(y)" stroke="black" />
          <text :x="50" :y="yScale(y) + 7" font-size="15" text-anchor="end">{{ y }}.0 m</text>
          <line :x1="61" :y1="yScale(y)" :x2="graphWidth" :y2="yScale(y)" stroke="#CCC" />
        </g>

        <line :x1="55" :y1="yScale(0)" :x2="graphWidth" :y2="yScale(0)" stroke="green" stroke-width="1.5" />

        <!-- Subdivisions in light grey -->
        <g v-for="y in yAxisValues" :key="'sub' + y">
          <line :x1="62" :y1="yScale(y - 0.5)" :x2="graphWidth" :y2="yScale(y - 0.5)" stroke="#DDD" />
        </g>

        <!-- Connections and Boosterpumps-->
        <g v-for="c in connections">
          <path :d="connectionPath(c)" stroke="#409EFF" stroke-width="2" fill="transparent" stroke-linecap="square" />
        </g>

        <!-- Components -->
        <g v-for="(component, index) in pathComponents" :key="index">
          <!-- use path_index+'-'+model.uid to force re-render when path changes -->
          <template v-if="component.type === 'model'">

            <rect :x="offsets[index] - 5" :y="0" :width="widths[index] + 10" :height="graphDimensions.height - graphDimensions.lowerOffset" fill="rgba(237.5, 189.9, 118.5, 0.1)" stroke="#E6A23C" v-if="component.uid == $project.scenario.editingModel && highlightEditingModel"/>

            <g :class="{'draggable': draggable(component)}">
            <component :is="'hydraulic-' + component.model.type" :config="component.model" :path="path" :position="index"
              :hydraulics="$project.designState.hydraulics.models[component.model.uid]"
              :uid="component.model.uid"
              @anchor="setAnchorpoints" 
              @size="setSize" 
              @booster="setBoosterElevation" 
              :upstream_elevation="upstreamElevation(index)"
              :downstream_elevation="downstreamElevation(index)"
              :dim="graphDimensions" 
              :offset="offsets[index]" 
              :width="widths[index]" 
              :key="path_index+'-'+component.model.uid" 
              @levels="setLevels"
              v-draggable="{start: startMove, move: move, end: endMove, focus: true, index: index}"
              >
            </component>
            </g>
            <text :x="offsets[index] + widths[index]/2" y="695" text-anchor="middle">{{ component.model.name }}</text>
            <template v-if="component.model.configuration.parameters.units">
              <text :x="offsets[index] + widths[index]/2" y="715" text-anchor="middle">N={{ component.model.configuration.parameters.units }}</text>
            </template>
          </template>
          <template v-else>
            <booster :config="component.booster" :dim="graphDimensions" :offset="offsets[index]" :width="widths[index]" :suggested-elevation="boosterElevation(index)" @size="setSize" @anchor="setAnchorpoints" :uid="component.uid" :key="path_index+'-'+component.uid"></booster>
          </template>
        </g>

        <g v-for="m in anchorpoints" v-if="debug">
          <circle :cx="m.in.x" :cy="m.in.y" r="3" fill="red" v-if="m.in" />
          <circle :cx="m.out.x" :cy="m.out.y" r="3" fill="red" v-if="m.out" />
        </g>
      
        <g v-for="l in levels" v-if="showLevels">
          <LevelIndicator :x="l.x" :y="l.y" :anchor="l.anchor" :direction="l.direction" :level="l.level" :pressure="true" />
        </g>
        <template v-for="m in modelLevels" v-if="showModelLevels">
          <LevelIndicator :x="l.x" :y="l.y" anchor="left" :direction="l.direction" :level="l.level" :pressure="l.pressure" v-for="l in m" />
        </template>
      </svg>
    </div>
  </div>
</template>

<script>
import waterpipe from '@/directives/waterpipe.js'
import roundPathCorners from '@/directives/roundpathcorners.js'
import Groundwater from '@/models/groundwater/hydraulic.vue'
import Booster from '@/components/Booster.vue'
import LevelIndicator from '@/components/LevelIndicator.vue'
import draggable from '../directives/draggable.js'
import throttle from 'lodash/throttle';

export default {
  components: {
    Groundwater,
    Booster,
    LevelIndicator
  },
  directives: {draggable},
  data() {
    return {
      debug: false,
      highlightEditingModel: false,
      path_index: 0,
      sizes: {},
      anchorpoints: {},
      boosterElevations: {},
      modelLevels: {},
      showLevels: true,
      showModelLevels: true,
      modelWidth: 150,
      boosterWidth: 40,
      graphDimensions: {
        width: 1300,  //px
        height: 750, //px
        upperOffset: 30, //px
        lowerOffset: 150, //px
        minY: -4,
        maxY: 8,
        gutter: 40,
      },
    }
  },
  watch: {
    sizes: {
      handler: function () {
        this.graphDimensions.minY = Math.min(100, ...Object.values(this.sizes).map(size => size.bottom));
        this.graphDimensions.maxY = Math.max(-100, ...Object.values(this.sizes).map(size => size.top));
      },
      deep: true
    },
    path_index() {
      // reset anchorpoints and sizes when path changes
      this.anchorpoints = {}
      this.sizes = {}
      // there is a 2000px maximum somehow -- max 9 models per path
      this.graphDimensions.width = this.pathComponents.reduce((width, component) => {
        return width + (component.type === 'model' ? this.modelWidth   : this.boosterWidth*1.5) + this.graphDimensions.gutter; 
      }, 200)

    }
  },

  computed: {
    stepY() {
      let range = this.graphDimensions.maxY - this.graphDimensions.minY 
      return (this.graphDimensions.height - this.graphDimensions.upperOffset - this.graphDimensions.lowerOffset) / range
    },
    levels() {
      if(Object.keys(this.anchorpoints).length == 0) return []
      let hydraulic_info = this.$project.designState.hydraulics

      let levels = []

      for(var idx=0; idx < this.pathComponents.length; idx++) {
        let m = this.pathComponents[idx]
        let m_next = this.pathComponents[idx+1]
        let m_prev = this.pathComponents[idx-1]

        // skip first and last model
        if(idx == this.pathComponents.length - 1) continue

        if(m.type === 'model') {

          // don't add levels for dosing models
          if(m.model.type == 'dosing') { continue }

          if(m.uid in hydraulic_info.models) {
            // add inlet level
            let model = hydraulic_info.models[m.uid]
            let level = model.head_in + model.booster_head
            let anchor = this.anchorpoints[m.uid]?.in
            let direction = 'nw'

            if(anchor)  {

              if(m_prev) {
                let y_prev = this.anchorpoints[m_prev.uid]?.out?.y
                direction = y_prev > anchor.y ? 'nw' : 'sw'
                if(anchor.anchor == 'bottom') { direction = 'sw' }
              }

              levels.push({x: anchor.x, y: anchor.y, level: level, anchor: anchor.anchor, above: true, direction: direction})
            }

            // add outlet level
            anchor = this.anchorpoints[m.uid]?.out

            if(m_next) {
              let y_next = this.anchorpoints[m_next.uid]?.in?.y
              direction = y_next > anchor.y ? 'ne' : 'se'
              if(anchor.anchor == 'bottom') { direction = 'se' }
              if(anchor.anchor == 'top') { direction = 'nw' }
            }

            level = (idx == 0) ? model.head_in : model.head_out
            console.log("level",m.model.type, level)
            levels.push({x: anchor.x, y: anchor.y, level: level, anchor: anchor.anchor, above: false, direction: direction})
          }
        }
      }
      
      return levels
    },

    graphWidth() {
      return this.pathComponents.reduce((width, component) => {
        return width + (component.type === 'model' ? this.modelWidth   : this.boosterWidth) + this.graphDimensions.gutter;
      }, 60)
    },
    // get all paths
    paths() {
      // Convert model UIDs to model objects in each path
      return this.$project.scenario.findAllProductPaths()
    },
    filteredPaths() {
      // paths with splitters removed
      return this.paths.map(path => {
        return path.filter(model => model.type !== 'splitter')
      })
    },
    // get the current path
    path() {
      return this.paths[this.path_index]
    },
    filteredPath() {
      return this.filteredPaths[this.path_index]
    },
    // generate array of y values for the y-axis
    yAxisValues() {
      return Array.from({ length: (this.graphDimensions.maxY - this.graphDimensions.minY + 1) }, (_, i) => i + this.graphDimensions.minY);
    },
    // generate array of connections with start and end points
    connections() {
      let connections = []
      if (Object.keys(this.anchorpoints).length == 0) return []
      for (let i = 0; i < this.pathComponents.length - 1; i++) {
        const src = this.pathComponents[i].uid
        const tgt = this.pathComponents[i + 1].uid
        const srcAnchor = this.anchorpoints[src]?.out
        const tgtAnchor = this.anchorpoints[tgt]?.in
        if(!srcAnchor || !tgtAnchor) continue

        connections.push({ 'src': srcAnchor, 'tgt': tgtAnchor })
      }

      return connections
    },
    widths() {
      return this.pathComponents.map(component => {
        if(component.type === 'model') {
          if(component.model.type == 'dosing') {
            return 30
          }
          return this.modelWidth
        }
        if(component.type === 'booster') {
          return this.boosterWidth
        }
      })
    },
    offsets() {
      return this.widths.reduce((acc, width, i) => {
        if (i === 0) {
          acc.push(55);
        } else {
          acc.push(acc[i-1] + this.widths[i-1] + this.graphDimensions.gutter);
        }
        return acc;
      }, []);
    },
    pathComponents() {
      // get all components (i.e. models and boosters) in the path
      let components = []
      let hydraulic_info = this.$project.designState.hydraulics

      for(let i = 0; i < this.path.length - 1; i++) {
        let srcModel = this.path[i]
        let tgtModel = this.path[i+1]
        if(srcModel.type === 'splitter') { continue } // skip splitters
        // add srcModel to components
        if(hydraulic_info.models[srcModel.uid].integrated_booster) {
          let elevation = srcModel.configuration.parameters.inlet_elevation
          if (isNaN(elevation)) {
            elevation = 0
          }
          components.push({
            'type': 'booster',
            'booster': {'booster_head': hydraulic_info.models[srcModel.uid].booster_head,
              'elevation': elevation
            },
            'uid': srcModel.uid + '-booster',
            'head': 12
          })
        }

        // if srcModel has an integrated booster, add it to components
        
        components.push({'type': 'model', 'model': srcModel, 'uid': srcModel.uid})
        // walk along the path until we find a non-splitter model or a booster
        let booster = false
        for(let j = i+1; j < this.path.length; j++) {
          let cid = this.path[j-1].uid + ' -> ' + this.path[j].uid + ' (product)'
          let connection = this.$project.designState.hydraulics.connections[cid]
          if(connection.booster) {
            // add booster to components
            components.push({'type': 'booster', 'booster': connection, 'uid': cid, 'head': connection.booster_head})
            break // stop after finding a booster
          }
          if(this.path[j].type !== 'splitter') { break } // stop if next model is not a splitter
        }
      }
      // append the last model to the components
      components.push({'type': 'model', 'model': this.path[this.path.length - 1], 'uid': this.path[this.path.length - 1].uid})
      return components
    }
  },
  methods: {
    draggable(component) {
      return component.model.configuration?.parameters?.inlet_elevation !== undefined
    },
    startMove(x0, y0, args, evt) {
      let elevation = this.pathComponents[args.index].model.configuration?.parameters?.inlet_elevation

      if (elevation !== undefined) {
        this.movingElevation = elevation
        return true
      }
      return false
    },
    applyElevation: throttle(function(index, diff) {
      this.pathComponents[index].model.configuration.parameters.inlet_elevation += diff
    }, 100),
    
    move(dx, dy, args, evt) {

      let step = this.stepY / 2

      if(Math.abs(dy) >= step) {
        let direction = dy > 0 ? -1 : 1
        this.applyElevation(args.index, 0.5 * direction)
      }

      return true
    },
    endMove(event) {
      this.$project.scenario.unsolved = true
      return true
    },
    boosterElevation(index) {
      if(Object.keys(this.boosterElevations).length == 0) return -1
      // get uid of previous component
      return this.boosterElevations[this.pathComponents[index-1].uid]
    },
    upstreamElevation(index) {
      if(index == 0) return undefined
      let component = this.pathComponents[index-1]
      return this.anchorpoints[component.uid]?.out?.y
    },
    downstreamElevation(index) {
      if(index == this.pathComponents.length - 1) return undefined
      let component = this.pathComponents[index+1]
      return this.anchorpoints[component.uid]?.in?.y
    },
    info(component) {
      if(component.type === 'model') {
        return component.model.name
      }
      if(component.type === 'booster') {
        return component.booster
      }
    },
    yScale(value) {
      let range = this.graphDimensions.maxY - this.graphDimensions.minY
      let scale = (this.graphDimensions.height - this.graphDimensions.upperOffset - this.graphDimensions.lowerOffset) / range
      let distance_from_top = this.graphDimensions.maxY - value
      return this.graphDimensions.upperOffset + distance_from_top * scale
    },
    setLevels(uid, levels) {
      this.modelLevels[uid] = levels
    },
    setBoosterElevation(uid, elevation) {
      this.boosterElevations[uid] = elevation
    },
    setSize(uid, dimensions) {
      // set the size of the model
      this.sizes[uid] = dimensions
    },
    setAnchorpoints(uid, points) {
      this.anchorpoints[uid] = points
    },
    connectionPath(connection) {

      let pathinfo = waterpipe.describe(connection.src, connection.tgt, {stubLength: 5})
      let path = waterpipe.makePath(pathinfo)

      var pathStr = "M" + (connection.src.x) + "," +
        (connection.src.y) + " "
      path.forEach((pnt) => {
        pathStr += "L" + (pnt.x) + "," +
          (pnt.y) + " "
      })


      return roundPathCorners(pathStr, 3)
    }


  }
}


</script>

<style>
.draggable {
  cursor: ns-resize;
}
.draggable:hover path {
  fill: #FCFCFF;
}
.hydraulic-container {
  position: relative;
}
.hydraulic-controls {
  padding: 10px;
}

.hydraulic-graph {
  margin-top: 10px;
  margin-bottom: 10px;
  position: relative;
  /* border: 1px solid black; */
}

.hydraulic-axis {
  background-color: white;
  position: absolute;
  left: 0px;
  top: 10px;
  z-index: 1000;
}
</style>
