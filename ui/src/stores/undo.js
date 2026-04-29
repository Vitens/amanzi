import {ref} from 'vue'

const undoStack = ref([])
const redoStack = ref([])

export function piniaUndoRedo(context) {


  // reset undo stack
  context.pinia.undoStack = []
  // reset undo stack
  context.pinia.storeMap = {}

  const maxStack = 100

  context.store.$pushUndo = (state) => {

    // clear redo stack
    context.store.redoStack.splice(0)

    context.pinia.storeMap[context.store.$id] = context.store

    // get global undoStack
    let stack = context.store.undoStack
    // if undo stack length < maxStack, push to stack, otherwise remove first element and push
    if (stack.length > maxStack) {
      stack.shift()
    }
    // make a copy of the state
    if(state) {
      stack.push({storeId: context.store.$id, state: JSON.parse(JSON.stringify(state))})
    } else {
      stack.push({storeId: context.store.$id, state: JSON.parse(JSON.stringify(context.store.$state))})
    }

  }

  context.store.$undo = () => {

    let stack = context.store.undoStack

    if (stack.length > 0) {

      let oldstate = stack.pop()
      // push current state to redo stack
      let store = context.pinia.storeMap[oldstate.storeId]
      context.store.redoStack.push({storeId: oldstate.storeId, state: JSON.parse(JSON.stringify(store.$state))})

      // get store 
      store.patchUndo(oldstate.state)
    }
  }

  context.store.$redo = () => {
    let stack = context.store.redoStack
    if(stack.length > 0) {
      let oldstate = stack.pop()
      // push current state to redo stack
      
      let store = context.pinia.storeMap[oldstate.storeId]
      context.store.undoStack.push({storeId: oldstate.storeId, state: JSON.parse(JSON.stringify(store.$state))})
      // get store 
      store.patchUndo(oldstate.state)
    }
  }


  return {undoStack: undoStack, redoStack: redoStack}


}