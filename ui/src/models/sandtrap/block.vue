<template></template>
<script>
const properties = {
  name: 'sandtrap',
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
      type: 'waste'
    }
  ]
}

export { properties }
</script>
<style>
.sandtrap {
  background-image: url('assets/block.png');
  background-position: 50% 80%;
  background-size: 100%;
  background-repeat: no-repeat
}
</style>
