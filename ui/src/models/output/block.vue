<template></template>
<script>
const properties = {
  name: 'output',
  category: 'main',
  sink: true,
  anchors: [
    {
      position: 'left',
      direction: 'in',
      type: 'product'
    }
  ]
}

export { properties }
</script>
<style>
.output {
  background-image: url('assets/block.png');
  background-position: 0px 6px;  
}
</style>