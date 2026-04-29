<template>
  <div 
    class="endpoint" :class="[info.position, info.type, endpointClass]" 
    @mousedown="startConnection" @mouseenter="hintConnection" @mouseleave="unhintConnection">
    <div class="endpoint-circle" v-if="unconnected"></div>
  </div>
</template>

<script>
export default {
  props: ['uid', 'info', 'connected'],
  data() { return {
    endpointClass: true 
  }},
  mounted() {
    this.$bus.on("valid-endpoint", (val) => this.endpointClass = val ? 'valid' : 'invalid')
  },
  computed: {
    unconnected() {
      if (this.info.optional) { return false }
      return !this.connected
    }
  },
  methods: {
    startConnection(evt) {
      evt.stopPropagation()
      evt.preventDefault()
      this.$bus.emit("start-connection", {evt: evt, uid: this.uid, info: this.info})
    },
    hintConnection(evt) {
      evt.stopPropagation()
      this.$bus.emit("hint-connection", {uid: this.uid, info: this.info})
    },
    unhintConnection(evt) {
      evt.stopPropagation()
      this.$bus.emit("unhint-connection", {uid: this.uid})
    }
  }
}
</script>

<style>
.endpoint {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #666;
  z-index: 12;
}
.endpoint:hover {
  background: #F88;
  cursor: crosshair;
}
.endpoint.valid:hover {
  background: green;
}

.endpoint.invalid:hover {
  background: #666 !important;
  cursor: not-allowed !important;
}

.endpoint.top { top: -4px; left: 50%; margin-left: -4px; }
.endpoint.left { left: -4px; top: 50%; margin-top: -4px; }
.endpoint.right { right: -4px; top: 50%; margin-top: -4px; }
.endpoint.bottom { bottom: -4px; left: 50%; margin-left: -4px; }

.endpoint.product {
  background: #1B78F6
}
.endpoint.waste {
  background: brown
}
.endpoint.flush {
  background: #409EFF
}

.endpoint-circle {
  position: absolute;
  width: 20px;
  height: 20px;
  top: -8px;
  left: -8px;
  border: 2px solid red;
  border-radius: 20px;
  pointer-events: none;
  animation: 1s ease-in-out 0s infinite alternate pulse;
  background-color: rgba(255, 0, 0, 0.1);
}
/* pulse red */
@keyframes pulse {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.15);
  }
}

</style>