<template>
  <el-tab-pane>
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <div id="plate-design">
      <div class="process">
        <div id="plate-process" :class="{'recirculation': params.recirculation > 0}">
          <Result name="influent" color="blue" :components="resultSet('influent')" />
          <Result name="effluent" color="green" :components="resultSet('effluent')" />
          <Result name="gas" color="red" :components="resultSet('gas')" />
        </div>
      </div>

      <el-row>
        <el-col :lg="12" :xl="8">
          <chart :xmin="0" :xmax="50" :datasets="phdata" :title="$t('models.plate.design.pH_and_SI')" xlabel="RQ [-]" ylabel="pH [-]" ylabel2="SI [-]" :ymin2="0.5" :ymax2="1" :designvalue="config.rq"></chart>
        </el-col>
        <el-col :lg="12" :xl="8">
          <chart :xmin="0" :xmax="50" :datasets="effluentData" :ymin="0" :ymin2="0" :title="$t('models.plate.design.effluent_quality')" :ymax="100" xlabel="RQ [-]" ylabel="CH4 [ug/l]" ylabel2="CO2 [mg/l]" :designvalue="config.rq"></chart>

        </el-col>
        <el-col :lg="12" :xl="8">
          <chart :xmin="0" :xmax="50" :datasets="oxygen" :title="$t('models.plate.design.oxygen')" ylabel="Volume (m3/h / Nm3/h)" xlabel="RQ [-]" :designvalue="config.rq"></chart>
        </el-col>
      </el-row>

    </div>

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
  components: {Chart, Result , Percent , DesignTables},
  props: ['config'],
  data() {
    return {
      wet: false
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
      ]
    },
    oxygen() {
      return [
        { label: 'O2', backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.output('charts', 'o2', 2, true)},
      ]
    },
  },
  methods: {
    output(group, key, precision=2, list=false) {
      // if key not in $runtime.designState, return '-'
      const resp = list ? [] : '-'
      if(!(group in this.$runtime.designState)) { return resp }
      if(!(key in this.$runtime.designState[group])) { return resp }

      let val = this.$runtime.designState[group][key]
      return list ? val : val.toFixed(precision)
    },
    resultSet(group) {
      if(!(group in this.$runtime.designState)) { return false }

      let data = this.$runtime.designState[group]

      if(group == 'gas') {
        return [
          {name: 'Volume', value: data.volume, units: 'Nm3/h'},
          {name: 'CH4', value: data.ch4, units: '%'},
          {name: 'CO2', value: data.co2, units: '%'},
          {name: 'N2', value: data.n2, units: '%'},
          {name: 'H2S', value: data.h2s, units: '%'},
          {name: 'O2', value: data.o2, units: '%'},
        ]

      }

      return [
        {name: 'pH', value: data.pH, units: '-'},
        {name: 'CO2', value: data.co2, units: 'mg/l'},
        {name: 'CH4', value: data.ch4, units: 'ug/l'},
        {name: 'H2S', value: data.h2s, units: 'mg/l'},
        {name: 'N2', value: data.n2, units: 'mg/l'},
        {name: 'O2', value: data.o2, units: 'mg/l'},
      ]
      
    },

  }
}


</script>
<style>

#plate-design {
  min-height: 800px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
}
#plate-process {
  position: relative;
  margin: auto;
  width: 800px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center
}
#plate-process.recirculation {
  background: url('./assets/process-recirculation.png') no-repeat center
}
#plate-process .influent {
  left: 0%;
  top: 30%;
}
#plate-process .effluent {
  left: 77%;
  bottom: 14%;
}
#plate-process .gas {
  left: 55%;
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
  left: 50px;
}

</style>