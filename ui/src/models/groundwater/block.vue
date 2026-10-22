<template>
</template>

<script>
const properties = {
  name: 'groundwater',
  category: 'main',
  source: true,
  anchors: [
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
.groundwater {
  background-image: url('assets/block.png');
  background-repeat: no-repeat;
  background-size: 90%;
  background-position: 5px 13px;
}

</style>