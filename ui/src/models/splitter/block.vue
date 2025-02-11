<template>
</template>
<script>

export default {
  name: 'block-splitter',
  mounted() {
  }
}


</script>
<style>
.splitter {
  width: 60px !important;
  height: 60px !important;
  outline: none !important;
  background: url('./assets/splitter.png') center center no-repeat;
  background-color: transparent !important;
  background-size: 75%;
}
.splitter .model-title {
  display: none;
}
.splitter.selected {
  background: url('./assets/splitter_selected.png') center center no-repeat;
  background-size: 75%;
}
</style>