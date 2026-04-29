<template>
  <div class="sandfiltration-logo" :class="modelClass">
    {{ model.configuration.parameters.spray }}

  </div>

</template>
<script>
export default {
  name: 'sandfiltration',
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
</script>

<style>
.sandfiltration-logo {
  width: 100px;
  height: 100px;
  background-image: url('assets/sandfilter.png');
  background-position: 0px 6px;  
}
.sandfiltration-logo.spray {
  background-image: url('assets/sandfilter-spray.png');
  background-position: 0px 13px;  
}
</style>