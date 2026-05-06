<template>
  <arrow></arrow>

  <svg id="connections">
    <connection :connection="c" v-for="c,i in $project.scenario.connections" :key="cid(c)" :index="i" :positions="positions" @update-path="updatePath" :allpaths="allPaths" ></connection>

    <connection v-if="newConnection.active" :connection="newConnection" :positions="positions" :allpaths="allPaths" ></connection>
  </svg>

</template>

<script>

import Arrow from './Arrow.vue'
import Connection from './Connection.vue'

export default {
  name: 'Connections',
  props: ['positions', 'display'],
  components: { Arrow, Connection },

  data() { return {
    allPaths: {},
    connectionClass: '',
    newConnection: {
      active: false,
      src: '',
      srcAnchor: 'right',
      customTgt: {},
      tgt: '',
      tgtAnchor: 'top',
      customPath: [],
      type: 'new',
      booster: false
    }
  }},

  mounted() {
    // connect to mitt global bus for events sent from model endpoints 
    this.$bus.on("start-connection", this.startConnection)
    this.$bus.on("hint-connection", this.hintConnection)
    this.$bus.on("unhint-connection", this.unhintConnection)
    this.$bus.on("delete-key", this.deleteConnection)
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

    findConnections(from, anchor) {
      return this.$project.scenario.connections.filter(conn => (conn.src == from && conn.srcAnchor == anchor))
    },

    translateEvt(evt) {
      // get coordinates relative to canvas
      let bounds = document.getElementById('canvas').getBoundingClientRect()
      return {x: (evt.clientX - bounds.left) / this.display.zoom, y: (evt.clientY - bounds.top) / this.display.zoom}
    },

    startConnection(args) {

      // validate new connection
      // only allow connections with 'out' direction; only single connection per anchor, except for flushing from reservoirs
      if(args.info.direction != 'out' || (this.findConnections(args.uid, args.info.position).length > 0 && !args.info.multiple)) {
        return false
      }

      this.newConnection.src = args.uid
      this.newConnection.srcAnchor = args.info.position
      this.newConnection.customTgt = this.translateEvt(args.evt)
      this.newConnection.active = true
      this.newConnection.type = args.info.type

      document.addEventListener('mousemove', this.moveConnection)
      document.addEventListener('mouseup', this.finishConnection)
    },
    moveConnection(evt) {
      evt.preventDefault()
      this.newConnection.customTgt = this.translateEvt(evt)
    },
    hintConnection(args) {
      if(!this.newConnection.active) {
        // check if new connections are allowed from that endpoint
        let valid = (args.info.direction == 'out' && (this.findConnections(args.uid, args.info.position).length == 0 || args.info.multiple))

        this.$bus.emit('valid-endpoint', valid)
        return
      }
      // only allow single flush connections
      if(args.info.type == 'flush' && this.findConnections(args.uid, args.info.position).length > 0) {
        this.$bus.emit('valid-endpoint', false)
        return
      }


      if(args.info.type == this.newConnection.type && args.info.direction == 'in' && !this.checkForLoop(args)) {
        this.checkForLoop(args)
        this.$bus.emit('valid-endpoint', true)
        this.newConnection.tgtAnchor = args.info.position
        this.newConnection.tgt = args.uid
      } else {
        this.$bus.emit('valid-endpoint', false)
      }
    },
    unhintConnection(args) {
      this.newConnection.tgt = ""
    },

    checkForLoop(args) {
      // check if the new connection makes a loop
      // get all connected blocks downstream
      var allConnectedModels = [this.newConnection.src]

      let walk = function(uid, type) {
        // walk through all downstream connections to find all connected models
        let from = this.$project.scenario.connections.filter(conn => (conn.tgt == uid && conn.type == type))
        for(var conn of from) {
          allConnectedModels.push(conn.src)
          walk(conn.src, conn.type)
        }
      }.bind(this)

      walk(this.newConnection.src, args.info.type)
      // fail if connection target is already in connected list
      return allConnectedModels.includes(args.uid)

    },

    finishConnection(evt) {
      evt.preventDefault()
      this.newConnection.active = false
      this.$bus.emit('connection-stop')

      if(this.newConnection.tgt != '') {
        let newConnection = _.cloneDeep(this.newConnection)
        delete newConnection.customTgt
        delete newConnection.active
        // create undo state
        this.$project.scenario.$pushUndo()

        this.$project.scenario.connections.push(newConnection)
        // set unsolved
        this.$project.scenario.unsolved = true
      }
      document.removeEventListener('mousemove', this.moveConnection)
      document.removeEventListener('mouseup', this.finishConnection)
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