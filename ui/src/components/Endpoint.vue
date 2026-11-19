<template>
  <div 
    class="endpoint" :class="[info.position, info.type, endpointClass, dragRole]"
    @mousedown="startConnection" @mouseenter="hintConnection" @mouseleave="unhintConnection">
    <div class="endpoint-circle" v-if="unconnected || dragRole"></div>
  </div>
</template>

<script>
export default {
  props: ['uid', 'info', 'connected'],
  data() { return {
    endpointClass: '',
    dragRole: '',
  }},
  mounted() {
    this.$bus.on('valid-endpoint', this.setValidity)
    this.$bus.on('connection-highlight', this.highlightConnection)
  },
  beforeUnmount() {
    this.$bus.off('valid-endpoint', this.setValidity)
    this.$bus.off('connection-highlight', this.highlightConnection)
  },
  computed: {
    unconnected() {
      if (this.info.optional) { return false }
      return !this.connected
    }
  },
  methods: {
    setValidity({ uid, position, valid }) {
      if (this.uid === uid && this.info.position === position) {
        this.endpointClass = valid ? 'valid' : 'invalid'
      }
    },
    highlightConnection(drag) {
      this.dragRole = ''
      if (!drag) return
      if (this.uid === drag.src && this.info.position === drag.srcAnchor) {
        this.dragRole = 'source'
      } else if (this.uid === drag.tgt && this.info.position === drag.tgtAnchor) {
        this.dragRole = 'target'
      }
    },
    startConnection(evt) {
      evt.stopPropagation()
      if (evt.button !== 0) return
      evt.preventDefault()
      this.$bus.emit("start-connection", {evt: evt, uid: this.uid, info: this.info})
    },
    hintConnection(evt) {
      evt.stopPropagation()
      this.$bus.emit("hint-connection", {uid: this.uid, info: this.info})
    },
    unhintConnection() {
      this.endpointClass = ''
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
.endpoint::before {
  content: '';
  position: absolute;
  inset: -4px;
}
.endpoint.source, .endpoint.target {
  z-index: 14;
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
.endpoint.source .endpoint-circle, .endpoint.target .endpoint-circle {
  border-color: #16783d;
  background-color: rgba(22, 120, 61, 0.15);
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
