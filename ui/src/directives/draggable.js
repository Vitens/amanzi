// Function to calculate the offset of the mouse event relative to an element
function eventToOffset(evt, elm, calculateScale=false){

  const bounds = elm.getBoundingClientRect()
  // console.log(elm)
  let stylewidth = elm.offsetWidth ? elm.offsetWidth : parseInt(elm.getAttribute('width'))

  let scale = calculateScale ? bounds.width / stylewidth : 1

  return {
    x: (evt.clientX - bounds.left) / scale,
    y: (evt.clientY - bounds.top) /scale
  }
}

// Define a Vue.js directive named v-draggable
export default {
  mounted(el, binding, vnode){

    // Get the directive arguments from the value property
    const args = binding.value

    // Initialize initial x and y positions
    var initX = 0, initY = 0

    // Function called when the mouse button is pressed down on the element
    function mouseDown(evt){
      // If the focus argument is set to true, set the focus to the element
      if(args && args.focus) {
        el.focus()
      }
      evt.preventDefault()
      evt.stopPropagation()

      // Calculate the initial offset of the mouse event
      const offset = eventToOffset(evt, el, args.scale)

      // Set the initial x and y positions
      initX = offset.x
      initY = offset.y

      // Call the start function if it exists, and prevent dragging if it returns false
      if(args.start && !args.start(initX, initY, args, evt)){
        return true
      }

      // Add mousemove and mouseup event listeners to the document
      document.addEventListener("mousemove", mouseMove, false)
      document.addEventListener("mouseup", mouseUp, false)
      return false
    }

    // Function called when the mouse is moved while the button is held down
    function mouseMove(evt){
      evt.preventDefault()
      evt.stopPropagation()

      // Calculate the current offset of the mouse event and the distance moved since the start
      const offset = eventToOffset(evt, el, args.scale)
      let dx = offset.x - initX,
        dy = offset.y - initY

      // If snap is set, round the distance moved to the nearest multiple of the snap value
      if(args.snap){
        dx = Math.round(dx / args.snap) * args.snap
        dy = Math.round(dy / args.snap) * args.snap
      }

      // Call the move function with the distance moved and other arguments
      if(Math.abs(dx) > 0 || Math.abs(dy) > 0) {
        args.move(dx, dy, args, evt, offset)
      }
    }

    // Function called when the mouse button is released
    function mouseUp(evt){
      evt.preventDefault()
      evt.stopPropagation()

      // Call the end function if it exists, with the distance moved and other arguments
      if(args.end){
        const offset = eventToOffset(evt, el, args.scale),
          dx = offset.x - initX,
          dy = offset.y - initY

        args.end(dx, dy, args, evt)
      }

      // Remove the mousemove and mouseup event listeners from the document
      document.removeEventListener("mousemove", mouseMove, false)
      document.removeEventListener("mouseup", mouseUp, false)
    }

    // Add a mousedown event listener to the element
    el.addEventListener("mousedown", mouseDown, false)
  }
}
