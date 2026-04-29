<template></template>
<script>
const properties = {
  name: 'waste',
  category: 'waste',
  anchors: [
    {
      position: 'left',
      direction: 'in',
      type: 'waste'
    }
  ]
}

export { properties }
</script>
<style>
.waste {
  background-image: url('assets/block.png');
  background-position: 14px 9px;  
  background-repeat: no-repeat;
  background-size: 80%;
}
</style>