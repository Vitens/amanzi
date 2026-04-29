<template>
</template>
<script>
const properties = {
  name: 'vacuum',
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
.vacuum {
  background-image: url('./assets/block.png');
  background-position: 8px 20px;
  background-size: 80%;
}
</style>