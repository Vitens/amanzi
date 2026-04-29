function eventToOffset(evt, elm){
  const bounds = elm.getBoundingClientRect()
  let scale = bounds.width / elm.offsetWidth
  return {
    x: (evt.clientX - bounds.left) / scale,
    y: (evt.clientY - bounds.top) /scale
  }
}

export default {
  mounted(el, binding, vnode){
    const args = binding.value

    el.addEventListener("wheel", (evt) => {
      evt.preventDefault()
      const offset = eventToOffset(evt, el),
        dz = evt.deltaY / (args.scale || 1000)

      args.zoom(-dz, offset.x, offset.y)
    }, false)
  }
}