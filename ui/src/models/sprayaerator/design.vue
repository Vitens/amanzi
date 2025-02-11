<template>
    <el-tab-pane id="sprayaerator-design">
      <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>
      <!-- <el-aside id="sprayaerator-config" class="design-config">
        <el-form label-position="top">
          <h3>Ontwerp</h3>
          <el-form-item label="Sauter diameter">
            <el-input type="number" v-model='config.sauter_diameter' :step="0.00001" :min="0.000001" :max="0.001">
              <template #append>
                  m
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="Fall height">
            <el-input type="number" v-model='config.fall_height' :step="0.1" :min="0.2" :max="3">
              <template #append>
                  m
              </template>
            </el-input>
          </el-form-item>
        </el-form>
  
      </el-aside> -->
      <el-main id="sprayaerator-design">
        <div class="process">
          <div id="sprayaerator-process">
            <Result name="influent" color="blue" :components="resultSet('influent')" />
            <Result name="effluent" color="green" :components="resultSet('effluent')" />
            <table class="hydraulics">

            </table>
          </div>
        </div>
  
        <el-row>
          <el-col :span="12">
            <h3>Hydraulisch</h3>
            <chart :datasets="removal_over_H" xlabel="Fall height" ylabel="Efficiency" title="" :ymin="0" :xmin="0" :xmax="4" :designvalue="config.fall_height" ></chart>
  
          </el-col>
          <el-col :span="12">
            <h3>Waterkwaliteit</h3>
            <el-select class="component-select" v-model="config.model_component">
              <el-option label="Koolstofdioxide" value="CO2"></el-option>
              <el-option label="Methaan" value="Mtg"></el-option>
            </el-select>  
            
            <chart :datasets="removal_over_d_sauter" xlabel="sauter diameter" ylabel="Efficiency" title="" :ymin="0" :xmin="0.000001" :xmax="0.001" :designvalue="config.sauter_diameter" xtype="logarithmic"></chart>
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
  // a little greener green
  green: '#67C23A',
  blue: '#409EFF',
  yellow: '#E6A23C',
  orange: '#b88230',
}


export default {
  components: {Chart, Result},
  props: ['config'],
  computed: {removal_over_H(){
    console.log(this.output('efficiency', 'Height', 2, true))
    return [
      { label: 'CO2', data: this.output('efficiency', 'Height', 2, true), backgroundColor: colors.red, borderColor: colors.red, showLine: true, pointRadius: 0, yAxisID: 'y'},
      { label: 'Mtg', data: this.output('efficiency', 'Height2', 2, true), backgroundColor: colors.green, borderColor: colors.green, showLine: true, pointRadius: 0, yAxisID: 'y'}
    ]
    },
    removal_over_d_sauter(){
      var trends = []
      
      // console.log(this.$project.designState.charts.efficiency_height)

      if(!this.$project.designState.efficiency) { return [] }
     
      var color_index = 0

      for (var height in this.$project.designState.efficiency.Sauter) {
        //console.log(this.$project.designState.charts.efficiency_height[height])
        var trend = {
          label: height + 'm',
          data: this.$project.designState.efficiency.Sauter[height],
          backgroundColor: Object.values(colors)[color_index],
          borderColor: Object.values(colors)[color_index],
          showLine: true,
          pointRadius: 0
        }
        color_index += 1
        trends.push(trend)
        
        
      }
      return trends
    }
  },

  methods: {
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

#sprayaerator-design {
  min-height: 200px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
}
#sprayaerator-process {
  position: relative;
  margin: auto;
  width: 900px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center
}
#sprayaerator-process .influent {
  left: 10%;
  top: 15%;
}
#sprayaerator-process .effluent {
  left: 65%;
  bottom: 2%;
}

#sprayaerator-process .hydraulics {
  position: absolute;
  top: 25%;
  left: 60%;
  font-size: 12px;
  width: 200px;
}
#sprayaerator-process .hydraulics tr td {
  margin: 0px;
  padding: 3px;
  border-bottom: 1px solid #eee;
}
#sprayaerator-process .hydraulics tr td:first-child {
  font-weight: bold;
  text-align: left;
  padding-right: 10px;
}
#sprayaerator-design .component-select {
  position: absolute;
  right: 10px;
  top: 10px;
} 


</style>
