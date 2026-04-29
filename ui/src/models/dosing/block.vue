<template>
  <div class="chemical" v-html="chemform(usedChem)">
  </div>
</template>
<script>
const properties = {
  name: 'dosing',
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
  name: 'dosing',
  computed: {
    usedChem() {
      return this.$t('models.dosing.parameters.options.' + (this.model.configuration.parameters.chemical ?? 'lye'))
    }
  }
}

export { properties }



</script>
<style>
.dosing {
  background: url('assets/block.png') no-repeat;
  background-position-x: 50%;
  background-position-y: -23px;
  background-color: transparent !important;
  width: 30px !important;
}
/* not .selected */

.dosing:not(.selected) {
  outline: 0px !important;
}

.dosing .model-title {
  display: none;
}
.dosing .chemical {
  position: absolute;
  top: -22px;
  left: 0px;
  right: 0px;
  text-align: center;
  font-size: 13px;
  background: #FFF;
  font-weight: bold;
}

</style>