<template>

  <percent v-model="config.fraction" label="Deelverhouding"></percent>

</template>
<script>
import Percent from '@/components/Percent.vue'

export default {
  name: 'config-splitter',
  components: { Percent },
  props: ['config'],
  data()  { return {
    fraction: 0
  }},
  mounted() {
    this.fraction = this.config.fraction*100
  },
  watch: {
    config: {
      handler(val) {
        this.fraction = val.fraction*100
      },
      deep: true
    },
    fraction(val) {
      this.config.fraction = val/100
    }
  }

}

</script>
<style>

</style>