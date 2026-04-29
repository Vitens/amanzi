function eventToOffset(evt, elm){
  const bounds = elm.getBoundingClientRect()
  let scale = bounds.width / elm.offsetWidth
  return {
    x: (evt.clientX - bounds.left) / scale,
    y: (evt.clientY - bounds.top) /scale
  }
}

function normalizeWheelDelta(evt) {
  // WheelEvent.deltaMode: 0=pixel, 1=line, 2=page
  const lineHeight = 16
  const pageHeight = window.innerHeight || 800
  let factor = 1
  if (evt.deltaMode === 1) factor = lineHeight
  if (evt.deltaMode === 2) factor = pageHeight
  return {
    x: evt.deltaX * factor,
    y: evt.deltaY * factor,
  }
}

function isLikelyMouseWheel(evt, delta) {
  // Most classic mouse wheels report line/page deltas.
  if (evt.deltaMode !== 0) return true

  // Pixel-mode wheel: large integer-only vertical steps are usually mouse wheels.
  // Trackpads more often emit fractional deltas and/or horizontal deltas.
  const absX = Math.abs(delta.x)
  const absY = Math.abs(delta.y)
  console.log(absX, absY)
  return absX === 0 && Number.isInteger(delta.y) && absY >= 10
}

export default {
  mounted(el, binding, vnode){
    const args = binding.value
    const gestureLockMs = args.gestureLockMs || 140
    let lockedGesture = null
    let lastGestureAt = 0

    const onWheel = (evt) => {
      evt.preventDefault()
      const offset = eventToOffset(evt, el)
      const delta = normalizeWheelDelta(evt)
      const scale = args.scale || 1000
      const pinchScale = args.pinchScale || 80
      const now = Date.now()

      if (!lockedGesture || now - lastGestureAt > gestureLockMs) {
        if (evt.ctrlKey) {
          lockedGesture = 'pinch'
        } else if (args.pan && !isLikelyMouseWheel(evt, delta)) {
          lockedGesture = 'pan'
        } else {
          lockedGesture = 'wheel'
        }
      }
      lastGestureAt = now

      // Trackpad pinch (commonly ctrl+wheel): zoom around cursor.
      if (lockedGesture === 'pinch') {
        const dz = delta.y / pinchScale
        args.zoom(-dz, offset.x, offset.y)
        return
      }

      // Pan for gestures classified as trackpad scroll.
      if (lockedGesture === 'pan' && args.pan) {
        args.pan(delta.x, delta.y, evt)
        return
      }

      // Traditional mouse wheel: keep zoom behavior.
      const dz = delta.y / scale
      args.zoom(-dz, offset.x, offset.y)
    }

    el.__zoomableWheelHandler = onWheel
    el.addEventListener("wheel", onWheel, { passive: false })
  },
  unmounted(el) {
    if (el.__zoomableWheelHandler) {
      el.removeEventListener("wheel", el.__zoomableWheelHandler)
      delete el.__zoomableWheelHandler
    }
  }
}