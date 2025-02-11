<template>
  <el-tab-pane id="membranedegassing-design">
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <div id="membranedegasser-process" :class="params.num_stages">

      <el-select class="display-mode" v-model="displayMode">
          <el-option value="total" :label="$t('models.membranedegassing.design.total_process')"></el-option>
          <el-option value="unit" :label="$t('models.membranedegassing.design.per_stack')"></el-option>
          <el-option value="membrane" :label="$t('models.membranedegassing.design.per_membrane')"></el-option>
          <el-option value="m3" :label="$t('models.membranedegassing.design.per_m3')"></el-option>
      </el-select>

      <el-input type="number" :min="1" v-model="displayFlow" :step="1" class="display-flow">
          <template #append>
            m<sup>3</sup>/h
          </template>
        </el-input>

      <Result name="influent" color="blue" :components="resultSet('influent')" />
      <Result name="gas1" color="red" :components="resultSet('gas1')" />
      <Result name="effluent1" color="orange" :components="resultSet('effluent1')" />
      <Result name="dosing1" color="red" :components="dosing(1)"/>
      <div v-if="params.num_stages == 'double'">
        <Result name="effluent2" color="green" :components="resultSet('effluent2')" />
        <Result name="gas2" color="red" :components="resultSet('gas2')" />
        <Result name="dosing2" color="red" :components="dosing(2)"/>
      </div>
    </div>
  </el-tab-pane>
</template>
<script>
import Chart from '@/components/Chart.vue'
import Result from '@/components/ResultBlock.vue'
import Percent from '@/components/Percent.vue'
import DesignTables from '@/components/DesignTables.vue'
import { update } from 'lodash'

const colors = {
  red: '#F56C6C',
  // a little greener green
  green: '#67C23A',
  blue: '#409EFF',
  yellow: '#E6A23C',
  orange: '#b88230',
}


export default {
  components: {Chart, Result, Percent, DesignTables},
  props: ['config'],
  data() {
    return {
      displayMode: 'unit',
      displayFlow: 1,
      wet: false
    }
  },
  computed: {
    params() {
      return this.config.parameters
    },
    stages() {
      return Array.from(Array(this.config.num_stages).keys()).map(x => x + 1)
    },
  },
  mounted() {
    this.updateDisplayFlow()
  },
  watch: {
    'params.units'() { this.updateDisplayFlow() },
    'params.membranes_per_stage'() { this.updateDisplayFlow() },
    'params.nominal_capacity'() { this.updateDisplayFlow() },

    displayMode(mode) {
      this.updateDisplayFlow()
    }
  },

  methods: {
    updateDisplayFlow() {
      // update displayflow
      switch(this.displayMode) {
        case 'm3':
          this.displayFlow = 1
          break
        case 'unit':
          this.displayFlow = this.params.nominal_capacity
          break
        case 'membrane':
          this.displayFlow = Math.round((this.params.nominal_capacity / this.params.membranes_per_stage) * 10) / 10
          break
        case 'total':
          this.displayFlow = this.params.nominal_capacity * this.params.units
          break
      }
    },
    output(group, key) {
      const resp = []
      if(!(group in this.$project.designState)) { return resp }
      if(!(key in this.$project.designState[group])) { return resp }
      return this.$project.designState[group][key]
    },
    dosing(stage) {
      let n2_dosing = this.params['n2_rq_stage_'+stage] * this.displayFlow
      let co2_dosing = this.params['co2_rq_stage_'+stage] * this.displayFlow
      return [
        {name: 'N2', value: n2_dosing, units: 'Nm3/h'},
        {name: 'CO2', value: co2_dosing, units: 'Nm3/h'},
      ]
    },
    resultSet(group) {

      if(!(group in this.$project.designState)) { return [] }

      let data = this.$project.designState[group]

      if(group == 'gas1' || group == 'gas2') {
        return [
          {name: 'Volume', value: data.volume * this.displayFlow, units: 'm3/h'},
          {name: '', value: data.normal_volume * this.displayFlow, units: 'Nm3/h'},
          {name: 'CH4', value: data.CH4, units: '%'},
          {name: 'CO2', value: data.CO2, units: '%'},
          {name: 'N2', value: data.N2, units: '%'},
        ]

      }

      return [
        {name: 'pH', value: data.pH, units: '-'},
        {name: 'CO2', value: data.CO2, units: 'mg/l'},
        {name: 'CH4', value: data.CH4, units: 'ug/l'},
        {name: 'N2', value: data.N2, units: 'mg/l'},
        {name: 'SI', value: data.SI, units: '-'},
      ]
      
    }

  }
}


</script>
<style>
#membranedegassing-design {
  min-height: 1000px;
}

#membranedegasser-process {
  position: relative;
  margin: auto;
  width: 1000px;
  height: 500px;
}
#membranedegasser-process.double {
  background: url('./assets/process.png') no-repeat center
}
#membranedegasser-process.single {
  background: url('./assets/process-single.png') no-repeat center
}
#membranedegasser-process .influent {
  left: 1.5%;
  top: 55%;
}
#membranedegasser-process .effluent2 {
  right: 1%;
  top: 1%;
}
#membranedegasser-process .effluent1 {
  left: 42.5%;
  top: 1%;
}
#membranedegasser-process .gas1 {
  left: 42.5%;
  bottom: 9%;
}
#membranedegasser-process .gas2 {
  right: 1%;
  bottom: 9%;
}
#membranedegasser-process .dosing1 {
  font-size: 12px;
  width: auto;
  left: 20%;
  top: 5%;
}
#membranedegasser-process .dosing1 label, #membranedegasser-process .dosing2 label {
  width: 30px;
}
#membranedegasser-process .dosing1 .value, #membranedegasser-process .dosing2 .value {
  width: 40px;
}
#membranedegasser-process .dosing1 .unit, #membranedegasser-process .dosing2 .unit {
  width: 40px;
}
#membranedegasser-process .dosing2 {
  font-size: 12px;
  width: auto;
  left: 61%;
  top: 5%;
}
#membranedegasser-process .display-mode {
  position: absolute;
  width: 150px;
  top: 0px;
  left: 0px;
  z-index: 5;
}
#membranedegasser-process .display-flow {
  width: 150px;
  position: absolute;
  top: 40px;
  left: 0px;
  z-index: 5;
}
.volume {
  border-bottom: none !important;
}
.gas-quality {
  position: relative;
}

</style>