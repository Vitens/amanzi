<template>
</template>

<script>
const properties = {
  name: 'membrane',
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
      position: 'bottom',
      direction: 'out',
      type: 'waste'
    }
  ]
}

export { properties }
</script>

<style>
.membrane {
  background-image: url('assets/block.png');
  background-repeat: no-repeat;
  background-size: 90%;
  background-position: 5px 13px;
}

</style>