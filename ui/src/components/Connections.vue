<template>
  <arrow></arrow>

  <svg id="connections">
    <connection :connection="c" v-for="c,i in $project.scenario.connections" :key="cid(c)" :index="i" :positions="positions" @update-path="updatePath" :allpaths="allPaths" ></connection>

    <connection v-if="newConnection" :connection="newConnection" :positions="positions" :allpaths="allPaths" ></connection>
  </svg>

</template>

<script>

import Arrow from './Arrow.vue'
import Connection from './Connection.vue'
import waterpipe from '../directives/waterpipe.js'

const SNAP_SCREEN_PX = 15

export default {
  name: 'Connections',
  props: ['positions', 'display'],
  components: { Arrow, Connection },

  data() { return {
    allPaths: {},
    newConnection: null,
  }},

  mounted() {
    // connect to mitt global bus for events sent from model endpoints 
    this.$bus.on("start-connection", this.startConnection)
    this.$bus.on("hint-connection", this.hintConnection)
    this.$bus.on("delete-key", this.deleteConnection)
  },
  beforeUnmount() {
    this.$bus.off('start-connection', this.startConnection)
    this.$bus.off('hint-connection', this.hintConnection)
    this.$bus.off('delete-key', this.deleteConnection)
    this.cancelConnection()
  },
  watch: {
    '$project.scenario'() {
      this.cancelConnection()
    },
    positions(positions) {
      const drag = this.newConnection
      if (drag && (!positions[drag.src] || (drag.tgt && !positions[drag.tgt]))) {
        this.cancelConnection()
      }
    },
  },
  methods: {
    deleteConnection() {
      this.$project.scenario.deleteConnection()
    },

    cid(connection) {
      return connection.src+" ("+connection.srcAnchor+")->"+
             connection.tgt+" ("+connection.tgtAnchor+")"
    },

    updatePath(cid, path, index) {
      this.allPaths[cid] = {path: path, index: index}
    },

    translateEvt(evt) {
      // get coordinates relative to canvas
      let bounds = document.getElementById('canvas').getBoundingClientRect()
      return {x: (evt.clientX - bounds.left) / this.display.zoom, y: (evt.clientY - bounds.top) / this.display.zoom}
    },

    isValidSource(uid, endpoint) {
      return endpoint.direction === 'out' && (endpoint.multiple ||
        !this.$project.scenario.connections.some(conn =>
          conn.src === uid && conn.srcAnchor === endpoint.position))
    },

    isValidTarget(uid, endpoint) {
      const { src, srcAnchor, type } = this.newConnection
      if (uid === src || endpoint.direction !== 'in' || endpoint.type !== type) return false
      const occupied = this.$project.scenario.connections.some(conn =>
        conn.tgt === uid && conn.tgtAnchor === endpoint.position &&
        (type === 'flush' || (conn.src === src && conn.srcAnchor === srcAnchor)))
      return !occupied && !this.createsLoop(uid)
    },

    createsLoop(target) {
      const { src, type } = this.newConnection
      const downstream = new Map()
      for (const conn of this.$project.scenario.connections) {
        if (conn.type !== type) continue
        if (!downstream.has(conn.src)) downstream.set(conn.src, [])
        downstream.get(conn.src).push(conn.tgt)
      }
      const reachable = new Set([target])
      for (const uid of reachable) {
        if (uid === src) return true
        for (const next of downstream.get(uid) || []) reachable.add(next)
      }
      return false
    },

    findSnapTarget(point) {
      // Keep the same hit radius on screen when the canvas is zoomed.
      let closestDistance = SNAP_SCREEN_PX / this.display.zoom
      let closest = null
      for (const model of this.$project.scenario.models) {
        const block = this.positions[model.uid]
        if (!block?.width || !block.height) continue
        for (const endpoint of this.modelspec[model.type].anchors) {
          const anchor = waterpipe.anchorPoint(block, endpoint.position)
          const distance = Math.hypot(anchor.x - point.x, anchor.y - point.y)
          if (distance < closestDistance && this.isValidTarget(model.uid, endpoint)) {
            closest = { uid: model.uid, position: endpoint.position }
            closestDistance = distance
          }
        }
      }
      return closest
    },

    startConnection({ evt, uid, info }) {
      if (this.newConnection || !this.isValidSource(uid, info)) return
      this.newConnection = {
        active: true,
        src: uid,
        srcAnchor: info.position,
        sourceEndpoint: info,
        startX: evt.clientX,
        startY: evt.clientY,
        type: info.type,
        tgt: '',
        tgtAnchor: 'top',
        customTgt: this.translateEvt(evt),
      }
      this.$bus.emit('connection-highlight', this.newConnection)
      document.addEventListener('mousemove', this.moveConnection)
      document.addEventListener('mouseup', this.finishConnection)
      document.addEventListener('keydown', this.cancelOnEscape)
      window.addEventListener('blur', this.cancelConnection)
    },

    moveConnection(evt) {
      if (!(evt.buttons & 1)) {
        this.cancelConnection()
        return
      }
      evt.preventDefault()
      const point = this.translateEvt(evt)
      const snap = this.findSnapTarget(point)
      const drag = this.newConnection
      const tgt = snap?.uid ?? ''
      const tgtAnchor = snap?.position ?? 'top'
      const targetChanged = tgt !== drag.tgt || tgtAnchor !== drag.tgtAnchor
      Object.assign(drag, { tgt, tgtAnchor, customTgt: snap ? null : point })
      if (targetChanged) this.$bus.emit('connection-highlight', drag)
    },

    hintConnection({ uid, info }) {
      const valid = this.newConnection ? this.isValidTarget(uid, info) : this.isValidSource(uid, info)
      this.$bus.emit('valid-endpoint', { uid, position: info.position, valid })
    },

    finishConnection(evt) {
      if (evt.button !== 0) return
      evt.preventDefault()
      const drag = this.newConnection
      // A click on the source alone shouldn't connect a nearby block.
      const moved = evt.clientX !== drag.startX || evt.clientY !== drag.startY
      const snap = moved && this.findSnapTarget(this.translateEvt(evt))
      this.cancelConnection()
      if (!snap || !this.isValidSource(drag.src, drag.sourceEndpoint)) return

      const scenario = this.$project.scenario
      scenario.$pushUndo()
      scenario.addConnection(drag.src, snap.uid, drag.srcAnchor, snap.position, drag.type)
      scenario.unsolved = true
      scenario.unsaved = true
    },

    cancelOnEscape(evt) {
      if (evt.key === 'Escape') this.cancelConnection()
    },

    cancelConnection() {
      if (!this.newConnection) return
      this.newConnection = null
      this.$bus.emit('connection-highlight', null)
      document.removeEventListener('mousemove', this.moveConnection)
      document.removeEventListener('mouseup', this.finishConnection)
      document.removeEventListener('keydown', this.cancelOnEscape)
      window.removeEventListener('blur', this.cancelConnection)
    },
  }

}
</script>

<style>
#connections {
  /* position: absolute; */
  z-index: -1;
  left: 0px;
  width: 100%;
  height: 100%;
}

#connections .active, #connections .valid {
  cursor: crosshair !important;
}


</style>
