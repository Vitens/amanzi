<template>
  <percent v-model="config.loss" label="Spoelverlies" :max="50"></percent>

</template>

<script>
import Percent from '@/components/Percent.vue'

export default {
  name: 'config-marblefiltration',
  components: { Percent },
  props: ['config'],
  data() {
    return {
      loss: 0
    }
  },
}
</script>
<style>

</style>