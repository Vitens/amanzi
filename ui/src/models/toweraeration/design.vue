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
            <el-option v-for="(value, label) in VOC_list()" :label="label" :value="label" :key="label"></el-option>
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
      
      // console.log(this.$project.designState.charts.efficiency_height)

      if(!this.$project.designState.charts) { return [] }
     
      var color_index = 0

      for (var height in this.$project.designState.charts.efficiency_height) {
        //console.log(this.$project.designState.charts.efficiency_height[height])
        var trend = {
          label: height + 'm',
          data: this.$project.designState.charts.efficiency_height[height],
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
          data: this.$project.designState.charts.VOC_concentration,
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
    }
  },
  methods: {
    VOC_list() {
      if(!this.$project.designState.charts) { return [] }

      return this.$project.designState.charts.VOC
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
}
#toweraeration-process {
  position: relative;
  margin: auto;
  width: 900px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center;
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