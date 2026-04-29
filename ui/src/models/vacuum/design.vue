<template>
    <el-tab-pane id="vacuum-design">
      <template #label>
        <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
      </template>

      <div class="process">

        <div id="vacuum-process">
          <el-select class="display-mode" v-model="displayMode">
              <el-option value="m3" :label="$t('models.vacuum.design.per_m3')"></el-option>
              <el-option value="unit" :label="$t('models.vacuum.design.per_unit')"></el-option>
              <el-option value="total" :label="$t('models.vacuum.design.total_process')"></el-option>
          </el-select>

        <el-input type="number" :min="1" v-model="displayFlow" :step="1" class="display-flow">
          <template #append>
            m<sup>3</sup>/h
          </template>
        </el-input>
          <Result name="influent" color="blue" :components="resultSet('influent')" />
          <Result name="effluent" color="green" :components="resultSet('effluent')" />
          <Result name="gas" color="red" :components="resultSet('gas_wet')" multiple :headers="[$t('models.vacuum.design.wet'), $t('models.vacuum.design.dry')]"/>
        </div>
      </div>

      <el-row>
        <el-col :span="12">
          <chart :xmin="0" :xmax="0.5" :datasets="phdata" :title="$t('models.vacuum.design.acidity-and-si')" :xlabel="$t('models.vacuum.design.vacuum-pressure')" ylabel="pH [-]" ylabel2="SI [-]" :ymin2="0.5" :ymax2="1" :designvalue="params.vacuum_pressure"></chart>
        </el-col>
        <el-col :span="12">
          <chart :xmin="0" :xmax="0.5" :datasets="effluentData" :title="$t('models.vacuum.design.effluent-quality')" :xlabel="$t('models.vacuum.design.vacuum-pressure')" ylabel="CH4, N2 & H2S [mg/l]" ylabel2="CO2 [mg/l]" :designvalue="params.vacuum_pressure"></chart>
        </el-col>
        <el-col :span="12">
          <chart :xmin="0" :xmax="0.5" :datasets="volumes" :title="$t('models.vacuum.design.wet-gas-volume')" ylabel="Volume (m3/h / Nm3/h)" :xlabel="$t('models.vacuum.design.vacuum-pressure')" :designvalue="params.vacuum_pressure"></chart>
        </el-col>
        <el-col :span="12" class="gas-quality">
          <!-- radio button group to toggle between dry and wet -->
          <el-radio-group v-model="wet" size="small" class="toggle">
            <el-radio-button :label="false">{{ $t('models.vacuum.design.dry') }}</el-radio-button>
            <el-radio-button :label="true">{{ $t('models.vacuum.design.wet') }}</el-radio-button>
          </el-radio-group>
          <chart :xmin="0" :xmax="0.5" :title="$t('models.vacuum.design.gas-quality')" :datasets="quality" ylabel="Vol %" :designvalue="params.vacuum_pressure" :xlabel="$t('models.vacuum.design.vacuum-pressure')"></chart>
        </el-col>
      </el-row>

    </el-tab-pane>


</template>
<script>
import Chart from '@/components/Chart.vue'
import Result from '@/components/ResultBlock.vue'
import Percent from '@/components/Percent.vue'
import DesignTables from '@/components/DesignTables.vue'

const colors = {
  red: '#F56C6C',
  // a little greener green
  green: '#67C23A',
  blue: '#409EFF',
  yellow: '#E6A23C',
  orange: '#b88230',
}


export default {
  components: {Chart, Result,Percent, DesignTables},
  props: ['config'],
  data() {
    return {
      wet: false,
      displayMode: 'total',
      displayFlow: 1,
    }
  },
  watch: {
    'params.units'() { this.updateDisplayFlow() },
    'params.nominal_capacity'() { this.updateDisplayFlow() },
    'displayMode'() {
      this.updateDisplayFlow()
    }
  },
  computed: {
    params() {
        return this.config.parameters
      },
    phdata() {
      return [
        { label: 'pH', backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.output('charts', 'pH', 2, true)},
        { label: 'SI', backgroundColor: colors.yellow, borderColor: colors.yellow, radius: 0, showLine: true, data: this.output('charts', 'SI', 2, true), yAxisID: 'y2' },
      ]
    },
    effluentData() {
      return [
        { label: 'CH4', backgroundColor: colors.green, borderColor: colors.green, radius: 0, showLine: true, data: this.output('charts', 'ch4', 2, true) },
        { label: 'CO2', backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.output('charts', 'co2', 2, true), yAxisID: 'y2' },
        { label: 'N2', backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.output('charts', 'n2', 2, true) },
        { label: 'H2S', backgroundColor: colors.orange, borderColor: colors.orange, radius: 0, showLine: true, data: this.output('charts', 'h2s', 2, true)},
      ]
    },
    volumes() {
      return [
        { label: 'Volume', backgroundColor: colors.green, borderColor: colors.green, radius: 0, showLine: true, data: this.output('charts', 'volume', 2, true) },
        { label: 'Normal volume', backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.output('charts', 'normal_volume', 2, true)},
      ]
    },
    quality() {

      const prefix = this.wet ? 'wet_' : 'dry_'

      var series = [
        { label: 'CH4', backgroundColor: colors.green, borderColor: colors.green, radius: 0, showLine: true, data: this.output('charts', prefix+'ch4', 2, true) },
        { label: 'CO2', backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.output('charts', prefix+'co2', 2, true) },
        { label: 'N2', backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.output('charts', prefix+'n2', 2, true) },
      ]
      if(this.wet) {
        series.push({ label: 'H2O', backgroundColor: colors.orange, borderColor: colors.orange, radius: 0, showLine: true, data: this.output('charts', 'wet_h2o', 2, true)})
      }

      return series

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
        case 'total':
          this.displayFlow = this.params.nominal_capacity * this.params.units
          break
      }
    },
    get_output(name) {
      if(this.$project.designState.outputs === undefined) { return "-" }
      if(!(name in this.$project.designState.outputs)) { return "-" }
      let output = this.$project.designState.outputs[name]
      return output.value.toFixed(output.precision)
    },
    output(group, key) {
      const resp = []
      if(!(group in this.$project.designState)) { return resp }
      if(!(key in this.$project.designState[group])) { return resp }
      return this.$project.designState[group][key]
    },
    resultSet(group) {


      if(!(group in this.$project.designState)) { return false }

      if(group == 'gas_dry' || group == 'gas_wet') {
        let wet = this.$project.designState.gas_wet
        let dry = this.$project.designState.gas_dry

        return [
          {name: 'Volume', value: [wet.volume * this.displayFlow, dry.volume * this.displayFlow], units: 'm3/h'},
          {name: '', value: [wet.normal_volume * this.displayFlow, dry.normal_volume * this.displayFlow], units: 'Nm3/h'},
          {name: 'CH4', value: [wet.ch4, dry.ch4], units: '%'},
          {name: 'CO2', value: [wet.co2, dry.co2], units: '%'},
          {name: 'N2', value: [wet.n2, dry.n2], units: '%'},
          {name: 'H2S', value: [wet.h2s, dry.h2s], units: '%'},
          {name: 'H2O', value: [wet.h2o, dry.h2o], units: '%'},
        ]

      }


      let data = this.$project.designState[group]

      return [
        {name: 'pH', value: data.pH, units: '-'},
        {name: 'CO2', value: data.co2, units: 'mg/l'},
        {name: 'CH4', value: data.ch4, units: 'ug/l'},
        {name: 'H2S', value: data.h2s, units: 'mg/l'},
        {name: 'N2', value: data.n2, units: 'mg/l'},
      ]
      
    }

  }
}


</script>
<style scoped>
#vacuum-design {
  min-height: 1000px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
  overflow: hidden;
}
#vacuum-process {
  position: relative;
  margin: auto;
  width: 800px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center
}
#vacuum-process .influent {
  left: 1%;
  top: 45%;
}
#vacuum-process .effluent {
  left: 64%;
  bottom: 2%;
}
#vacuum-process .gas {
  left: 64%;
  top: 17%;
}
.volume {
  border-bottom: none !important;
}
.gas-quality {
  position: relative;
}
.gas-quality .toggle {
  position: absolute;
  top: 30px;
  left: 30px;
}
#vacuum-process .display-mode {
  position: absolute;
  width: 150px;
  top: 10px;
  left: 0px;
  z-index: 5;
}
#vacuum-process .display-flow {
  width: 150px;
  position: absolute;
  top: 50px;
  left: 0px;
  z-index: 5;
}

</style>