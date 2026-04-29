<template>
  <div id="energy" class="quickresult">
    <copy-button target="#energy table"></copy-button>
    <h1><i class='fa fa-bolt'></i>{{$t('ui.sidebar.energy.label')}}</h1>
    <table>
      <tr>
        <td>{{$t('ui.sidebar.energy.specific_consumption_production')}}:</td>
        <td>{{ specific_consumption_production }}</td>
        <td class="units">kWh/m<sup>3</sup></td>
      </tr>
      <tr>
        <td>{{$t('ui.sidebar.energy.specific_consumption_distribution')}}:</td>
        <td>{{ specific_consumption_distribution }}</td>
        <td class="units">kWh/m<sup>3</sup></td>
      </tr>
      <tr>
        <td rowspan="2">{{$t('ui.sidebar.energy.total')}}:</td>
        <td>{{ total_specific_consumption }}</td>
        <td class="units">MWh/j</td>
      </tr>
      <tr>
        <td style="display: none;"></td>
        <td>{{ total_consumption }}</td>
        <td class="units">MWh/j</td>
      </tr>
    </table>
  </div>
</template>
<script>
import CopyButton from '@/components/CopyButton.vue';

export default {
  components: {CopyButton},
  computed: {
    specific_consumption_production() {
      if(!this.$project.state.energy) { return "-" }
      return _.round(this.$project.state.energy.specific_consumption_production, 3)
    },
    specific_consumption_distribution() {
      if(!this.$project.state.energy) { return "-" }
      return _.round(this.$project.state.energy.specific_consumption_distribution, 3)
    },
    total_consumption() {
      if(!this.$project.state.energy) { return "-" }
      return _.round(this.$project.state.energy.total_consumption, 0)
    },
    total_specific_consumption() {
      if(!this.$project.state.energy) { return "-" }
      return _.round(this.$project.state.energy.specific_consumption, 3)
    }
  }

}
</script>
<style>
</style>