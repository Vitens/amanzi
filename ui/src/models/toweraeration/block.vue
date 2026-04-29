<template></template>
<script>
const properties = {
  name: 'toweraeration',
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
    }
  ]
}

export { properties }
</script>
<style>
.toweraeration {
  background-image: url('./assets/block.png');
  background-position: 0px 10px;  
  background-size: 100%;
  background-repeat: no-repeat;
}
</style>