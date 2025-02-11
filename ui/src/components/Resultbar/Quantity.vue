<template>
  <div id="quantity" class="quickresult">
    <copy-button target="#quantity table"></copy-button>
    <h1><i class='fa fa-tint'></i>{{$t('ui.sidebar.waterquantity.label')}}</h1>
    <table>
      <tr>
        <td>{{$t('ui.sidebar.waterquantity.abstraction')}}:</td>
        <td>{{ abstraction }}</td>
        <td class="units">Mm<sup>3</sup>/j</td>
      </tr>
      <tr>
        <td>{{$t('ui.sidebar.waterquantity.delivery')}}:</td>
        <td>{{ distribution }}</td>
        <td class="units">Mm<sup>3</sup>/j</td>
      </tr>
      <tr>
        <td rowspan="2">{{$t('ui.sidebar.waterquantity.loss')}}:</td>
        <td>{{ absolute_loss }}</td>
        <td class="units">Mm<sup>3</sup>/j</td>
      </tr>
      <tr>
        <td style="display: none;"></td> <!-- dummy td for formatting -->
        <td>{{ relative_loss }}</td><td class="units">&percnt;</td>
      </tr>
    </table>
  </div>
</template>
<script>
import CopyButton from '@/components/CopyButton.vue';

export default {
  components: {CopyButton},
  computed: {
    abstraction() {
      if(!this.$project.state.quantity) { return "-" }
      return _.round(this.$project.state.quantity.abstraction, 2)
    },
    distribution() {
      if(!this.$project.state.quantity) { return "-" }
      return _.round(this.$project.state.quantity.distribution, 2)
    },
    absolute_loss() {
      if(!this.$project.state.quantity) { return "-" }
      return _.round(this.$project.state.quantity.abstraction - this.$project.state.quantity.distribution, 2)
    },
    relative_loss() {
      // water losses as a percentage of the total water abstracted
      if(!this.$project.state.quantity) { return "-" }
      return _.round((this.$project.state.quantity.abstraction - this.$project.state.quantity.distribution) / this.$project.state.quantity.abstraction * 100, 2)

    }

  }

}
</script>
<style>
</style>