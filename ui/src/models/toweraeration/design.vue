<template>
  <el-tab-pane id="toweraeration-design">
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <el-main id="toweraeration-design">
      <div class="process">
        <div id="toweraeration-process">
          <Result name="influent" color="blue" :components="resultSet('influent')" />
          <Result name="effluent" color="green" :components="resultSet('effluent')" />
          <table class="hydraulics">
            <tr><td>{{ $t('models.toweraeration.outputs.F-Factor') }}</td><td>{{ output('model', 'F') }}</td><td>Pa<sup>0.5</sup></td></tr>
            <tr><td>{{ $t('models.toweraeration.outputs.liquid_loading') }}</td><td>{{ output('model', 'liquid_load') }}</td><td>m<sup>3</sup>/m<sup>2</sup>/u</td></tr>
            <tr><td>{{ $t('models.toweraeration.outputs.flooding_factor') }}</td><td>{{ output('model', 'flooding_factor') }}</td><td>&percnt;</td></tr>
            <tr><td>{{ $t('models.toweraeration.outputs.liquid_holdup') }}</td><td>{{ output('model', 'liquid_holdup') }}</td><td>&percnt;</td></tr>
            <tr><td>{{ $t('models.toweraeration.outputs.pressuredrop') }}</td><td>{{ output('model', 'pressure_drop') }}</td><td>mbar/m</td></tr>
          </table>
        </div>
        <div class="voc-panel" v-if="vocRows.length">
          <div class="voc-scroll">
            <table class="voc-table">
              <thead>
                <tr>
                  <th>{{ $t('models.toweraeration.design.component') }}</th>
                  <th>{{ $t('models.toweraeration.design.influent') }}</th>
                  <th>{{ $t('models.toweraeration.design.effluent') }}</th>
                  <th>{{ $t('models.toweraeration.design.removal') }}</th>
                  <th>{{ $t('models.toweraeration.design.unit') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in vocRows" :key="row.name">
                  <td class="name">{{ row.name }}</td>
                  <td class="influent">{{ formatConc(row.influent) }}</td>
                  <td class="effluent">{{ formatConc(row.effluent) }}</td>
                  <td>{{ formatRemoval(row.removal) }}</td>
                  <td>{{ row.unit }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <el-row>
        <el-col :span="12">
          <h3>{{ $t('models.toweraeration.design.hydraulics') }}</h3>
          <div v-if="checkforflodding" class="text-bar">{{ $t('models.toweraeration.design.column_is_flooding') }}</div>

          <chart :datasets="flooding" title="" :xlabel="$t('models.toweraeration.design.water_capacity')" :ylabel="$t('models.toweraeration.design.air_capacity')"   xtype="logarithmic" ytype="logarithmic" designvalue="" targetvalue=""></chart>

        </el-col>
        <el-col :span="12">
          <h3>{{ $t('models.toweraeration.design.water_quality') }}</h3>
          <el-select class="component-select" v-model="config.model_component">
            <el-option :label="$t('models.toweraeration.outputs.CO2')" value="CO2"></el-option>
            <el-option :label="$t('models.toweraeration.outputs.Methane')" value="Mtg"></el-option>
            <el-option v-for="(value, label) in vocList" :label="label" :value="label" :key="label"></el-option>
          </el-select>
 
          <chart :datasets="removal_over_rq" xlabel="RQ" ylabel="Efficiency" title="" :ymax="1" :xmin="0" :xmax="100" :designvalue="params.rq" :ymin2="0" ylabel2="Effluent VOC in mg/l" :reverseaxis2=true ></chart>

        </el-col>

      </el-row>


    </el-main>

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
  components: {Chart, Result, Percent, DesignTables},
  props: ['config'],
  
  computed: {
    params() {
      return this.config.parameters
    },
    VOC() {
      // console.log(config.influent)
      return 'Test1'
    },
    vocRows() {
      const influent = this.$runtime.designState?.influent?.VOC
      if (!influent) { return [] }

      const effluent = this.$runtime.designState.effluent?.VOC || {}
      const meta = this.$project.scenario?.metaData?.customMicroComponents?.VOC || []
      const byName = {}
      for (const item of meta) {
        if (item?.name) { byName[item.name] = item }
      }

      return Object.keys(influent)
        .filter(name => influent[name] > 0)
        .map(name => {
          const inf = influent[name]
          const eff = effluent[name] ?? 0
          const metaItem = byName[name] || {}
          return {
            name,
            influent: inf,
            effluent: eff,
            removal: inf ? (1 - eff / inf) * 100 : 0,
            unit: metaItem.unit || 'mg/l',
          }
        })
    },
    flooding() {

      return [
        { label: 'Flooding',backgroundColor: colors.red, borderColor: colors.red, data: this.output('charts', 'flooding', 2, true), showLine: true, pointRadius: 0, yAxisID: 'y'},
        { label: 'Operating',backgroundColor: colors.green, borderColor: colors.green, data: this.output('charts', 'operating', 2, true), showLine: true, pointRadius: 0, yAxisID: 'y'},
        { label: 'Werkpunt',backgroundColor: colors.orange, borderColor: '#000', data: this.output('charts', 'working_point', 2, true), showLine: false, pointRadius: 6, pointStyle: 'rectRot', yAxisID: 'y'}
      ]
    },
    checkforflodding(){
      return this.output('charts', 'column_is_flooding', 2, true)
    },
    removal_over_rq(){
      var trends = []
      
      // console.log(this.$runtime.designState.charts.efficiency_height)

      if(!this.$runtime.designState.charts) { return [] }
     
      var color_index = 0

      for (var height in this.$runtime.designState.charts.efficiency_height) {
        //console.log(this.$runtime.designState.charts.efficiency_height[height])
        var trend = {
          label: height + 'm',
          data: this.$runtime.designState.charts.efficiency_height[height],
          backgroundColor: Object.values(colors)[color_index],
          borderColor: Object.values(colors)[color_index],
          showLine: true,
          pointRadius: 0,
          yAxisID: 'y'

        }
        color_index += 1
        trends.push(trend)
        
        
      }
      trends[trends.length-1].backgroundColor = 'red'
      trends[trends.length-1].borderColor = 'red'
      trends[trends.length-1].borderDash = [5,5]
      
      var VoC = {
          label: '',
          plugins:{legend: {    display: false}},
          data: this.$runtime.designState.charts.VOC_concentration,
          backgroundColor: 'white',
          borderColor: 'white',
          showLine: false,
          pointRadius: 0,
          yAxisID: 'y2'

        }
      trends.push(VoC)

      //  for t in range(3):
      //   k.append(label: 'Height = 1m',backgroundColor: colors.red, borderColor: colors.red, data: this.output('charts', 'efficiency_height', 2, true), showLine: true, pointRadius: 0, yAxisID: 'y')
      return trends
    },

    effluentData() {
      return []
    },
    vocList() {
      const charts = this.$runtime.designState?.charts
      if (!charts || !charts.VOC) { return {} }
      return charts.VOC
    }
  },
  watch: {
    vocList: {
      immediate: true,
      handler(voc) {
        if (Object.keys(voc).length > 0) { return }
        const selected = this.config?.model_component
        if (selected === 'CO2' || selected === 'Mtg') { return }
        this.config.model_component = 'CO2'
      }
    }
  },
  methods: {
    formatConc(val) {
      const num = Number(val)
      if (val === undefined || val === null || Number.isNaN(num)) { return '-' }
      const abs = Math.abs(num)
      if (abs === 0) { return '0.00' }
      if (abs < 0.01) { return num.toPrecision(3) }
      if (abs > 1000) { return num.toFixed(0) }
      if (abs > 100) { return num.toFixed(1) }
      return num.toFixed(2)
    },
    formatRemoval(val) {
      if (val === undefined || val === null || Number.isNaN(Number(val))) { return '-' }
      return Number(val).toFixed(1) + '%'
    },
    output(group, key, precision=2, list=false, index=false) {
      // if key not in $runtime.designState, return '-'
      const resp = list ? [] : '-'
      if(!(group in this.$runtime.designState)) { return resp }
      if(!(key in this.$runtime.designState[group])) { return resp }

      let val = this.$runtime.designState[group][key]
      if(index) {
        val = val[index]
      }
      return list ? val : val.toFixed(precision)
    },
    resultSet(group) {
      if(!(group in this.$runtime.designState)) { return false }

      let data = this.$runtime.designState[group]

      return [
        {name: 'pH', value: data.pH, units: '-'},
        {name: 'CO2', value: data.CO2, units: 'mg/l'},
        {name: 'CH4', value: data.CH4, units: 'mg/l'},
        {name: 'O2', value: data.O2, units: 'mg/l'},
      ]
      
    },
    editingModel() {
      return this.$project.scenario.models.find(m => m.uid == this.$project.scenario.editingModel)}



  }
}


</script>
<style>

#toweraeration-design {
  min-height: 200px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  box-sizing: border-box;
}
#toweraeration-process {
  position: relative;
  width: 900px;
  height: 400px;
  flex: 0 0 auto;
  background: url('./assets/process.png') no-repeat center;
}
.voc-panel {
  width: 620px;
  max-width: 100%;
  margin-top: 12px;
}
.voc-panel h3 {
  margin: 0 0 6px;
}
.voc-scroll {
  max-height: 240px;
  overflow: auto;
}
.voc-table {
  border: 1px solid #666;
  border-spacing: 0;
  border-collapse: separate;
  width: 100%;
  color: #000;
  font-size: 13px;
}
.voc-table thead th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: #337ecc;
  color: white;
  font-size: 14px;
  text-align: center;
  padding: 5px;
  border-bottom: 1px solid #333;
}
.voc-table th:first-child,
.voc-table td.name {
  text-align: left;
  white-space: normal;
}
.voc-table td {
  padding: 5px 18px;
  text-align: center;
  border-bottom: 1px solid #BBB;
  border-left: 1px solid #BBB;
  white-space: nowrap;
}
.voc-table td:first-child {
  border-left: none;
}
.voc-table tr:last-child td {
  border-bottom: none;
}
.voc-table td.influent {
  background-color: #d9ecff;
}
.voc-table td.effluent {
  background-color: #e1f3d8;
}
#toweraeration-process .influent {
  left: 10%;
  top: 15%;
}
#toweraeration-process .effluent {
  left: 65%;
  bottom: 2%;
}

#toweraeration-process .hydraulics {
  position: absolute;
  top: 25%;
  left: 60%;
  font-size: 12px;
  width: 200px;
}
#toweraeration-process .hydraulics tr td {
  margin: 0px;
  padding: 3px;
  border-bottom: 1px solid #eee;
}
#toweraeration-process .hydraulics tr td:first-child {
  font-weight: bold;
  text-align: left;
  padding-right: 10px;
}
#toweraeration-design .component-select {
  position: absolute;
  right: 10px;
  top: 10px;
  width:50%;
}
.text-bar {
  position: absolute;
  z-index: 10%;
  left: 235px;
  top: 150px;
  width: 10%;
  text-align: center;
  color: white;
  background-color: rgba(238, 10, 10, 0.7);
}

</style>