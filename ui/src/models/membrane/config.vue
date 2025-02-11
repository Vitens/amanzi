<template>
  <percent v-model="config.recovery" label="Recovery" :max="99"></percent>

</template>

<script>
import Percent from '@/components/Percent.vue'

export default {
  name: 'config-membrane',
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