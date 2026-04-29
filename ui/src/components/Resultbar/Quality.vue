<template>
  <div id="quality" class="quickresult">
    <h1><i class='fa fa-flask'></i>{{ $t('ui.sidebar.waterquality.label') }}</h1>
    <copy-button target="#quality table"></copy-button>
    <table>
      <tr v-for="parameter in parameters" :class="evaluate(parameter)">
        <td>{{ $t('ui.sidebar.waterquality.'+parameter.name) }}</td>
        <td>{{ Math.round(parameter.value*100)/100 }}</td>
        <td>{{ parameter.units }}</td>
      </tr>
    </table>
  </div>
</template>
<script>

import CopyButton from '@/components/CopyButton.vue';

export default {
  components: {CopyButton},
  computed: {
    parameters() {
      return this.$runtime.solveState.quality
    }
  },
  methods: {
    evaluate(parameter) {
      // check ul and ut 
      if(parameter.ul && parameter.value > parameter.ul) {
        return 'red'
      }
      if(parameter.ll && parameter.value < parameter.ll) {
        return 'red'
      }
      if(parameter.ut && parameter.value > parameter.ut) {
        return 'orange'
      }
      if(parameter.lt && parameter.value < parameter.lt) {
        return 'orange'
      }
      return 'green'

    }
  }


}
</script>
<style>

</style>