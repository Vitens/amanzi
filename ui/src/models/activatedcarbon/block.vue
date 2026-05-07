<template></template>
<script>
const properties = {
  name: 'activatedcarbon',
  category: 'main',
  hidden: false,
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
      direction: 'in',
      type: 'flush'
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
.activatedcarbon {
  background-image: url('assets/block.png');
  background-position: 0px 6px;  
}
</style>