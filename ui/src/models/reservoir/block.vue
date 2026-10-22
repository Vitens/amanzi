<template></template>
<script>
const properties = {
  name: 'reservoir',
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
      position: 'top',
      direction: 'out',
      type: 'flush',
      multiple: true,
      optional: true
    }
  ]
}

export { properties }
</script>
<style>
.reservoir {
  background-image: url('assets/block.png');
  background-position: 0px 6px;  
}
</style>