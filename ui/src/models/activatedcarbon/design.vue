<template>
    <el-tab-pane id="acfilter-design">
      <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
      </template>
      
      <el-main  v-loading='loading'  id="acfilter-design">
        <div class="process">
          <div id="acfilter-process">
            <Result name="influent" color="blue" :components="resultSet('influent')" />
            <Result name="effluent" color="green" :components="resultSet('effluent')" />
            <table class="hydraulics">
              <tr><td>Regeneration</td><td>{{ output('model', 'regeneration') }}</td><td>days</td></tr>
              <tr><td>EBCT</td><td>{{ output('model', 'EBCT') }}</td><td>min</td></tr>
              <tr><td>Volume</td><td>{{ output('model', 'Volume') }}</td><td>m<sup>3</sup></td></tr>
            </table>
          </div>
        </div>
  
        <el-row v-if="params.advanced">
          <el-col :span="12">
            
            <chart :datasets="removal_over_time" title="" xlabel="Bedvolumes" ylabel="Concentration " :designvalue="params.interval" :targetvalue="1" :ymax="1" :ymin="0"></chart>
  
          </el-col>
          <el-col :span="12">
 
            
            <chart :datasets="Efficency" title="" xlabel="Bedvolumes" ylabel="PEQ" :designvalue="params.replacement_interval" :targetvalue="1" :ymin="0"></chart>
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
  green: '#67C23A',
  blue: '#409EFF',
  yellow: '#E6A23C',
  orange: '#b88230',
  purple: '#800080',
  pink: '#FFC0CB',
  brown: '#A52A2A',
  black: '#000000',
  white: '#F0F0FF',
  teal: '#008080',
  navy: '#000080',
  maroon: '#800000',
  lime: '#00FF00',
  olive: '#808000',
  cyan: '#00FFFF',
  silver: '#C0C0C0',
  gray: '#808080',
  magenta: '#FF00FF',
  indigo: '#4B0082',
};


export default {
  components: {Chart, Result, Percent , DesignTables},
  props: ['config'],
  data() {
    return {
      loading: true,
      simple: true,
    }
    },

  computed: {
    params() {
      return this.config.parameters
    },
    Efficency() {
      return [
        {label: 'PEQ', data: this.output('model', 'peqPFAS', 2, true), color: colors.red,showLine: true, pointRadius: 0, yAxisID: 'y'},
        {label: 'Sum4', data: this.output('model', 'sum4PFAS', 2, true), color: colors.blue,showLine: true, pointRadius: 0, yAxisID: 'y'},
        {label: 'Sum20', data: this.output('model', 'sum20PFAS', 2, true), color: colors.green,showLine: true, pointRadius: 0, yAxisID: 'y'}

      ]
    },
    removal_over_time(){
      var trends = []
      
      // console.log(this.$runtime.designState.charts.efficiency_height)

      if(!this.$runtime.designState.model) { return [] }
     
      var color_index = 0

      for (var compound in this.$runtime.designState.model.breakthrough) {
        //console.log(this.$runtime.designState.charts.efficiency_height[height])
        var trend = {
          label: compound,
          data: this.$runtime.designState.model.breakthrough[compound],
          backgroundColor: Object.values(colors)[color_index],
          borderColor: Object.values(colors)[color_index],
          showLine: true,
          pointRadius: 0,
          yAxisID: 'y'

        }
        color_index += 1
        trends.push(trend)
        
      }
      return trends},
    Efficency2() {
      return [
        {label: 'C', data: this.output('model', 'breakthrough', 2, true), color: colors.green,showLine: true, pointRadius: 0, yAxisID: 'y'},
      ]
    },
    Ebct(){
        return [
            {label: 'EBCT', data: this.output('model', 'EBCT', 2, true), color: colors.red},
        ]
    },
    effluentData() {
      return []
    },
  },
  watch: {
    // config: {
    //   handler(){
    //     this.loading = true
    //     console.log(this.loading)
    //   },
    //   deep: true
    // },
    '$runtime.designState': {
      handler(){
        this.loading = false
      },
      deep: true
    }
  },
  
  methods: {
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

      let result = []
      for (let [key, value] of Object.entries(data)) {
        result.push({name: key, value: value, units: 'ng/l'}) // adjust this line as needed
      }
      return result
      
    },
    handleSwitch(){
      this.simple = !params.advanced
      
    }

  }
}


</script>
<style>
#acfilter-design {
min-height: 200px;
}
.process {
border-radius: 5px;
width: 100%;
border: 1px solid #CCC;
}
#acfilter-process {
position: relative;
margin: auto;
width: 1000px;
height: 400px;
background: url('./assets/process.png') no-repeat center
}
#acfilter-process .influent {
left: 15%;
top: 15%;
}
#acfilter-process .effluent {
left: 65%;
bottom: 2%;
}

#acfilter-process .hydraulics {
position: absolute;
top: 5%;
left: 70%;
font-size: 12px;
width: 200px;
}
#acfilter-process .hydraulics tr td {
margin: 0px;
padding: 3px;
border-bottom: 1px solid #eee;
}
#acfilter-process .hydraulics tr td:first-child {
font-weight: bold;
text-align: left;
padding-right: 10px;
}
#acfilter-design .component-select {
position: absolute;
right: 10px;
top: 10px;
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