<template>
  <div class="chemical" v-html="chemform(usedChem)">
  </div>
</template>
<script>
export default {
  props: ['model'],
  computed: {
    usedChem() {
      return this.model.configuration.parameters.chemical ?? 'NaOH'
    }
  }
}



</script>
<style>
.dosing {
  background: url('assets/dosing.png') no-repeat;
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