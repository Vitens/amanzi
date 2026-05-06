<template>
</template>
<script>
const properties = {
  name: 'splitter',
  category: 'main',
  anchors: [
    {
      position: 'left',
      direction: 'in',
      type: 'product'
    },
    {
      position: 'right',
      direction: 'out',
      type: 'product'
    },
    {
      position: 'bottom',
      direction: 'out',
      type: 'product'
    }
  ]
}

export { properties }


</script>
<style>
.splitter {
  width: 60px !important;
  height: 60px !important;
  outline: none !important;
  background: url('./assets/block.png') center center no-repeat;
  background-color: transparent !important;
  background-size: 75%;
}
.splitter .model-title {
  display: none;
}
.splitter.selected {
  background: url('./assets/splitter_selected.png') center center no-repeat;
  background-size: 75%;
}
</style>