<template>
</template>
<script>
const properties = {
  name: 'membranedegassing',
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
.membranedegassing {
  background-image: url('./assets/block.png');
  background-repeat: no-repeat;
  background-position: 15px 23px;
  background-size: 75%;
}
</style>