<template>
  <span class="pipeline-length">
    {{ length }}
  </span>
  <span class="pipeline-diameter">
    ⌀{{ diameter }} mm
  </span>
</template>

<script>
const properties = {
  name: 'pipeline',
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

export default {
  props: ['model'],
  name: 'pipeline',
  computed: {
    length() {
      let length = this.model.configuration.parameters.pipe_length
      if (length < 1000) {
        return _.round(length, 0) + ' m'
      } else {
        return _.round(length / 1000, 1) + ' km'
      }
    },
    diameter() {
      return this.model.configuration.parameters.pipe_inner_diameter
    }

  }
}

export { properties }
</script>


<style>
.pipeline {
  width: 60px !important;
  height: 60px !important;
  outline: none !important;
  background-image: url('./assets/block.png');
  background-color: transparent !important;
  background-size: 100%;
}
.pipeline .model-title {
  display: none;
}
.pipeline.selected {
  background-image: url('./assets/pipe-selected.png');
}
.pipeline-length {
  display: inline-block;
  width: 100%;
  text-align: center;
  font-size: 12px;
  color: #333;
}
.pipeline-diameter {
  display: inline-block;
  width: 100%;
  margin-top: 15px;
  text-align: center;
  font-size: 12px;
  color: #333;
}
</style>