<template>
  <div class="marblefiltration-logo" :class="modelClass">
    {{ model.configuration.parameters.spray }}

  </div>

</template>
<script>
const properties = {
  name: 'marblefiltration',
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

export default {
  name: 'marblefiltration',
  props: ['model'],
  computed: {
    modelClass() {
      if (this.model?.configuration?.parameters?.spray) {
        return 'spray'
      }
      return ''
    }
  }
}

export { properties }
</script>
<style>

.marblefiltration-logo {
  width: 100px;
  height: 100px;
  background-image: url('./assets/block.png');
  background-position: 0px 6px;  
}
.marblefiltration-logo.spray {
  background-image: url('./assets/marblefilter.png');
  background-position: 0px 13px;  
}
</style>