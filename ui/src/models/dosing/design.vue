<template>
  <el-tab-pane>
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <el-main id="dosing-design">
      <div class="process">
        <div class="dosing-warning" v-if="warning">
          <i class="fa fa-warning"></i> &nbsp;{{ $t('models.dosing.design.setpoint_warning') }}
        </div>
        <div id='dosing-process'>
          <div id="dosing-tank" :class="chemicalClass"></div>
          <div id="dosing-chemical" v-html="chemical" :class="chemicalClass"></div>
          <div id="dosage">{{ dosage }} mmol/l</div>
          <Result name="influent" color="blue" :components="resultSet('influent')" />
          <Result name="effluent" color="green" :components="resultSet('effluent')" />
        </div>
      </div>

      <el-row>
        <el-col :lg="12" :sm="12">
          <chart :xmin="0" :xmax="2" :datasets="phdata" :title="$t('models.dosing.design.dosingcurve_pH')" :xlabel="$t('models.dosing.design.dosing')+ ' mmol'" :designvalue="dosage" ylabel="pH [-]" :targetvalue="target('pH')"></chart>
        </el-col>
        <el-col :lg="12" :sm="12">
          <chart :xmin="0" :xmax="2" :datasets="sidata" :title="$t('models.dosing.design.dosingcurve_SI')" :xlabel="$t('models.dosing.design.dosing')+ ' mmol'" :designvalue="dosage" ylabel="SI [-]" :targetvalue="target('SI')"></chart>
        </el-col>
        <!-- AgCO2 -->
        <el-col :lg="12" :sm="12">
          <chart :xmin="0" :xmax="2" :datasets="aggco2" :title="$t('models.dosing.design.dosingcurve_AggCO2')" :xlabel="$t('models.dosing.design.dosing')+ ' mmol'" :designvalue="dosage" ylabel="AggCO2 [mg/l]" :targetvalue="target('AggCO2')"></chart>
        </el-col>
        <!-- tacc90 -->
        <el-col :lg="12" :sm="12">
          <chart :xmin="0" :xmax="2" :datasets="ccpp90" :title="$t('models.dosing.design.dosingcurve_CCPP90')" :xlabel="$t('models.dosing.design.dosing')+ ' mmol'" :designvalue="dosage" ylabel="TACC90 [mmol/l]" :targetvalue="target('CCPP90')"></chart>
        </el-col>
      </el-row>

    </el-main>

  </el-tab-pane>

</template>
<script>
import Chart from '@/components/Chart.vue'
import Result from '@/components/ResultBlock.vue'

const colors = {
  red: '#F56C6C',
  green: '#67C23A',
  blue: '#409EFF',
  yellow: '#E6A23C',
  orange: '#b88230',
  purple: '#9c27b0',
}

export default {
  components: {Chart, Result},
  props: ['config'],
  data() {
    return {
    }
  },
  watch: {
    'config.parameter'() {
      this.params.setpoint = this.setpointRange.default
    }
  },
  computed: {
    params() {
      return this.config.parameters
    },
    setpointRange() {
      switch(this.params.setpoint_parameter) {
        case 'pH':
          return {min: 6, max: 9, step: 0.1, default: 8}
        case 'si':
          return {min: -2, max: 2, step: 0.1, default: 0}
        case 'agco2':
          return {min: 0, max: 10, step: 0.1, default: 0}
        case 'ccpp90':
          return {min: 0, max: 5, step: 0.1, default: 0.4}
      }
    },
    warning() {
      return this.$runtime.designState.warning
    },
    setpointUnits() {

      switch(this.params.setpoint_parameter) {
        case 'pH':
          return 'pH'
        case 'si':
          return 'SI'
        case 'agco2':
          return 'mg/l'
        case 'ccpp90':
          return 'mmol/l'
      }
      return '-'
    },
    ccpp90() {
      if(!this.$runtime.designState.charts) { return [] }
      return [{ label: 'Doseercurve TACC90', borderColor: colors.orange, backgroundColor: colors.orange, data: this.$runtime.designState.charts.ccpp90, showLine: true, radius: 0}]
    },
    aggco2() {
      if(!this.$runtime.designState.charts) { return [] }
      return [{ label: 'Doseercurve AggCO2', borderColor: colors.purple, backgroundColor: colors.purple, data: this.$runtime.designState.charts.agco2, showLine: true, radius: 0}]
    },
    phdata() {
      if(!this.$runtime.designState.charts) { return [] }
      return [{ label: 'Doseercurve pH', borderColor: colors.red, backgroundColor: colors.red, data: this.$runtime.designState.charts.ph, showLine: true, radius: 0}]
    },
    sidata() {
      if(!this.$runtime.designState.charts) { return [] }
      return [{ label: 'Doseercurve SI', borderColor: colors.blue, backgroundColor: colors.blue, data: this.$runtime.designState.charts.si, showLine: true, radius: 0}]
    },
    dosage() {
      if(this.params.mode == 'constant') { 
        if(!this.params.dosage) { return 0 }
        return this.params.dosage
      }
      if(!this.$runtime.designState.calculated_dosage) { return 0 }
      return _.round(this.$runtime.designState.calculated_dosage, 2)
    },
    chemical() {
      if(!this.params.chemical) { return "" }
      return this.chemform(this.$t('models.dosing.parameters.options.' + this.params.chemical)) 
    },
    chemicalClass() {
      if(!this.params.chemical) { return "" }
      const chem = this.params.chemical
      // return acid, base or other
      // acid: CO2, HCl, H2SO4
      // base: NaOH, Ca(OH)2, CaCO3
      // other: O2, FeCl3, MnCl2

      switch(chem) {
        case 'co2':
        case 'hcl':
        case 'h2so4':
          return 'acid'
        case 'lye':
        case 'lime':
        case 'calcite':
          return 'base'
        default:
          return 'other'
      }

    }

  },
  methods: {
    resultSet(name) {

      if(!(name in this.$runtime.designState)) {
        return []
      }

      let data = this.$runtime.designState[name]

      let resp = [
        {'name': 'pH', 'units': '-', 'value': data.ph},
        {'name': 'SI', 'units': '-', 'value': data.si},
        {'name': 'O2', 'units': 'mg/l', 'value': data.o2},
        {'name': 'AgCO2', 'units': 'mg/l', 'value': data.agco2},
        {'name': 'TACC90', 'units': 'mmol/l', 'value': data.ccpp90}
      ]
      return resp
    },

    target(parameter) {
      if(this.params.mode != 'setpoint') {
        return null
      }
      return parameter == this.params.setpoint_parameter ? this.params.setpoint : null
    }


  }

}
</script>
<style>

#dosing-design {
  min-height: 800px;
}
#dosing-process {
  position: relative;
  margin: auto;
  width: 1000px;
  height: 300px;
  background: url('./assets/process.png') no-repeat center
}
#dosing-chemical {
  position: absolute;
  color: white;
  font-size: 16px;
  text-shadow: 0px 0px 5px #553300;
  left: 36.5%;
  text-align: center;
  width: 93px;
  top: 35%;
}

#dosage {
  position: absolute;
  left: 51%;
  top: 50%;
  color: #333;
  background-color: #FAFAFA;
  border: 1px solid #AAA;
  padding: 2px 8px;
  border-radius: 5px;
}

#dosing-design .influent {
  top: 55%;
  left: 18%;
}
#dosing-design .effluent {
  top: 55%;
  left: 82%;
  margin-left: -160px;
}

#dosing-tank {
  position: absolute;
  left: 366px;
  top: 70px;
  width: 91px;
  height: 87px;
  border-radius: 0px 0px 10px 10px;
}
#dosing-tank.base {
  background: rgb(153, 74, 206);
}
#dosing-tank.acid {
  background: rgb(255, 165, 0);
}
#dosing-tank.other {
  background: #007ACC;
}

#dosing-design .dosing-warning {
  position: absolute;
  left: 0px;
  right: 0px;
  background-color: var(--el-color-warning);
  padding: 6px;
  color: var(--el-color-white);
  font-weight: bold;
  font-size: 14px;
  text-align: center;
}


</style>