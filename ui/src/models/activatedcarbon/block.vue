<template></template>
<script>
const properties = {
  name: 'activatedcarbon',
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
.activatedcarbon {
  background-image: url('assets/block.png');
  background-position: 0px 6px;  
}
</style>