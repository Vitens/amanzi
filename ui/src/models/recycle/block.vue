<template></template>
<script>
const properties = {
  name: 'recycle',
  category: 'waste',
  anchors: [
    {
      position: 'left',
      direction: 'in',
      type: 'waste'
    },
    {
      position: 'right',
      direction: 'out',
      type: 'product'
    },
    {
      position: 'bottom',
      direction: 'out',
      type: 'waste'
    }
  ]
}

export { properties }
</script>
<style>
.recycle {
  background-image: url('assets/block.png');
  background-position: 50% 80%;
  background-size: 60%;
  background-repeat: no-repeat
}
</style>
