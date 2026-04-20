<template>
  <el-tab-pane id="cascade-design">
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <div class="process"> 
      <div id="cascade-process">
        <table id="cascade-table">
          <thead>
            <tr>
              <th></th>
              <th v-for="h in headers" v-html="chemform(h)"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in steps">
              <td>{{$t('models.cascade.design.step') }} {{s}}</td>
              <td v-for="k in headers"> {{ table(k, s-1) }}</td>
            </tr>
          </tbody>
        </table>
        <Result name="influent" color="blue" :components="resultSet('influent')" />
        <Result name="effluent" color="green" :components="resultSet('effluent')" />
      </div>
    </div>

    <el-row>
      <el-col :xl="8" :lg="12">
        <chart :xmin="1" :datasets="phdata" :title="$t('models.cascade.design.pHcourse')" :xlabel="$t('models.cascade.design.steps')+` (h = ${params.step_height} m)`" ylabel="pH [-]" :designvalue="params.number_of_steps" ></chart>
      </el-col>
      <el-col :xl="8" :lg="12">
        <chart :xmin="1" :datasets="effluentData" :ymin="0" :ymin2="0" :title="$t('models.cascade.design.effluentQuality')"  :xlabel="$t('models.cascade.design.steps')+` (h = ${params.step_height} m)`" ylabel="CH4, O2 [mg/l]" :designvalue="params.number_of_steps" ylabel2="CO2 [mg/l]"></chart>

      </el-col>
      <el-col :xl="8" :lg="12">
        <chart :xmin="1" :xmax="8" :datasets="efficiencyData" :title="$t('models.cascade.design.yield')" ylabel="%" :xlabel="$t('models.cascade.design.steps')" :designvalue="params.number_of_steps"></chart>
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
  components: {Chart, Result, Percent , DesignTables},
  props: ['config'],
  computed: {
    params() {
      return this.config.parameters
    },
    headers() {
      return ['pH', 'O2', 'CO2', 'CH4']
    },
    steps() {
      // array from 1 to config.steps
      let steps = this.params.number_of_steps ? parseInt(this.params.number_of_steps) : 1
      let resp = Array.from(Array(steps).keys()).map(x => x+1)
      return resp
    },
    phdata() {
      return [
        { label: 'pH', backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.output('charts', 'pH', 2, true), pointRadius: 4},
      ]
    },
    effluentData() {
      return [
        { label: 'CH4', backgroundColor: colors.green, borderColor: colors.green, pointRadius: 3, showLine: true, data: this.output('charts', 'CH4', 2, true), pointStyle: 'rect', borderWidth: 2},
        { label: 'CO2', backgroundColor: colors.blue, borderColor: colors.blue, pointRadius: 3, showLine: true, data: this.output('charts', 'CO2', 2, true), yAxisID: 'y2', pointStyle: 'triangle', borderWidth: 2},
        { label: 'O2', backgroundColor: colors.red, borderColor: colors.red, pointRadius: 3, showLine: true, data: this.output('charts', 'O2', 2, true), borderWidth: 2},
      ]
    },
    efficiencyData() {
      return [
        { label: 'CH4', backgroundColor: colors.green, borderColor: colors.green, pointRadius: 3, showLine: true, data: this.output('charts', 'CH4_eff', 2, true), pointStyle: 'rect', borderWidth: 2},
        { label: 'CO2', backgroundColor: colors.blue, borderColor: colors.blue, pointRadius: 3, showLine: true, data: this.output('charts', 'CO2_eff', 2, true), pointStyle: 'triangle', borderWidth: 2},

        { label: 'O2', backgroundColor: colors.red, borderColor: colors.red, pointRadius: 3, showLine: true, data: this.output('charts', 'O2_eff', 2, true), borderWidth: 2},
      ]
    },
  },
  methods: {
    table(key, index) {
      let out = this.output('charts', key, 2, true)[index]
      if (out == undefined) { return '-' }
      return out.y.toFixed(2)
    },
    output(group, key, precision=2, list=false, index=false) {
      // if key not in $project.designState, return '-'
      const resp = list ? [] : '-'
      if(!(group in this.$project.designState)) { return resp }
      if(!(key in this.$project.designState[group])) { return resp }

      let val = this.$project.designState[group][key]
      if(index) {
        val = val[index]
      }
      return list ? val : val.toFixed(precision)
    },
    resultSet(group) {
      if(!(group in this.$project.designState)) { return false }

      let data = this.$project.designState[group]

      return [
        {name: 'pH', value: data.pH, units: '-'},
        {name: 'CO2', value: data.CO2, units: 'mg/l'},
        {name: 'CH4', value: data.CH4, units: 'mg/l'},
        {name: 'O2', value: data.O2, units: 'mg/l'},
      ]
      
    },

  }
}


</script>
<style>

#cascade-design {
  min-height: 200px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
}
#cascade-table {
  position: absolute;
  top: 5px;
  right: -50px;
  border-collapse: collapse;
  border-spacing: 0;
  font-size: 13px;
  text-align: center;
}
#cascade-table tr td:first-child {
  font-weight: bold;
  text-align: left;
  padding-right: 10px;
}
#cascade-table td {
  padding: 5px 10px;
}
#cascade-table td {
  border-bottom: 1px solid #CCC;
}
#cascade-process {
  position: relative;
  margin: auto;
  width: 1000px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center
}
#cascade-process .influent {
  left: -2%;
  top: 10%;
}
#cascade-process .effluent {
  left: 79%;
  bottom: 5%;
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