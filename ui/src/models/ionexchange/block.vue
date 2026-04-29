<template>
</template>

<script>
const properties = {
  name: 'ionexchange',
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
.ionexchange {
  background-image: url('assets/block.png');
  background-repeat: no-repeat;
  background-size: 90%;
  background-position: 5px 13px;
}

</style>