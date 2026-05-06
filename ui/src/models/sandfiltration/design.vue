<template>
  <el-tab-pane id="sandfilter-design">
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <div class="process">
      <div id="sandfilter-process" :doublelayer="params.dual_media" :sprayer="params.spray">
        <table id="sandfilter-table">
          <tr>
            <th></th>
            <th v-for="h in headers" v-html="chemform(h)"></th>
          </tr>
          <tr v-for="s,i in steps">
            <td>{{i+1}}. {{ $t('models.filtration.design.' + s) }}</td>
            <td v-for="k in headers" :class="validate(s, k)">{{ output(s, k, 2) }}</td>
          </tr>
        </table>

        <Result name="influent" color="blue" :components="resultSet('influent')">
        </Result>
        <Result v-if="params.spray" name="spray" color="blue" :components="resultSet('spray')" class="spray">
        </Result>
        <Result name="effluent" color="green" :components="resultSet('manganese_removal')">
        </Result>

      </div>

    </div>

    <el-row class="depth-charts">
      <el-col :span="3">
        <ul>
          <li v-for="s in steps">
            {{ $t('models.filtration.design.' + s) }}
          </li>
        </ul>
      </el-col>
      <el-col :span="4">
        <chart :datasets="dataset('pH')" :ylabels="steps" xlabel="pH [-]" :title="$t('models.filtration.design.pH')">
        </chart>
      </el-col>
      <el-col :span="4">
        <chart :datasets="dataset('O2', 'blue')" :ylabels="steps" :xmin="0" :xlabel="$t('models.filtration.design.O2')" :title="$t('models.filtration.design.O2_consumption')">

        </chart>
      </el-col>
      <el-col :span="5">
        <chart :datasets="datasets(['Fe','NH4', 'Mn'], ['red','green','blue'])" :ylabels="steps" :xmin="0" xlabel="Fe, NH4, Mn [mg/l]" :title="$t('models.filtration.design.filtration')">
        </chart>
      </el-col>
      <el-col :span="4">
        <chart :datasets="dataset('CO2', 'purple')" :ylabels="steps" :xmin="0" xlabel="CO2 [mg/l]" :title="$t('models.filtration.design.acid_formation')">
          </chart>
      </el-col>
      <el-col :span="4">
        <chart :datasets="dataset('HCO3', 'orange')" :ylabels="steps" xlabel="HCO3 [mg/l]" :title="$t('models.filtration.design.bicarbonate')">
          </chart>
      </el-col>
      </el-row>

  </el-tab-pane>

</template>
<script>
import Chart from '@/components/DepthChart.vue'
import Result from '@/components/ResultBlock.vue'
import Percent from '@/components/Percent.vue'
import DesignTables from '@/components/DesignTables.vue'

const colors = {
  red: '#F56C6C',
  green: '#67C23A',
  blue: '#409EFF',
  yellow: '#E6A23C',
  orange: '#b88230',
  purple: '#9c27b0',
}

export default {
  components: {Chart, Result, Percent , DesignTables},
  props: ['config'],
  data() {
    return {
    }
  },
  computed:{
  sandFiltrationStyle() {
    let pic = '';
    if (this.$runtime.designstate.parameters.spray == 'spray') {
      if (this.$runtime.designstate.parameters.dual_media) {
        pic = './assets/process-spray-double.png';
      } else {
        pic = './assets/process-spray.png';
      }
    } else {
      if (this.$runtime.designstate.parameters.dual_media) {
        pic = './assets/process-double.png';
      } else {
        pic = './assets/process.png';
      }
    }
    return pic;
  }
},

  methods: {
    validate(step, key) {
      if(key != 'O2') { return ''}
      let val = this.output(step, key)
      if (parseFloat(val) < 0.2) { return 'warning' }
    },
    output(step, key, precision) {
      if(this.$runtime.designState.values == undefined) { return "-" }

      if(!(step in this.$runtime.designState.values)) { return "-" }

      let val = this.$runtime.designState.values[step][key]
      
      return val > 100 ? val.toFixed(0) : val.toFixed(precision)
    },
    datasets(labels, colors) {
      let datasets = []
      for(var i in labels) {
        datasets.push(this.dataset(labels[i], colors[i])[0])
      }
      return datasets
    },
    dataset(label, color='red') {

      // compile data
      let data = []
      for(var i in this.steps) {
        var s = this.steps[i]
        var y = this.steps.length - i
        data[i] = {x:_.round(this.values[s][label], 2), y:y}
      }

      return [{
        'label': label,
        'borderColor': colors[color],
        'backgroundColor': colors[color],
        'radius': 3,
        'showLine': true,
        'data': data
      }]
    },

    resultSet(name) {

      if (this.values == undefined) { return [] }
      if(!(name in this.$runtime.designState.values)) { return [] }

      let inf = this.$runtime.designState.values[name]
      
      if (name ==='spray') {
        var resp = [
          {'name': 'pH', 'units': '-', 'value': inf['pH']},
          {'name': 'O2', 'units': 'mg/l', 'value': inf['O2']},
          {'name': 'CO2', 'units': 'mg/l', 'value': inf['CO2']},
          {'name': 'CH4', 'units': 'μg/l', 'value': inf['CH4']},
        ]
      }
      else{
      var resp = [
        {'name': 'pH', 'units': '-', 'value': inf['pH']},
        {'name': 'O2', 'units': 'mg/l', 'value': inf['O2']},
        {'name': 'CH4', 'units': 'μg/l', 'value': inf['CH4']},
        {'name': 'CO2', 'units': 'mg/l', 'value': inf['CO2']},
        {'name': 'Fe', 'units': 'mg/l', 'value': inf['Fe']},
        {'name': 'NH4', 'units': 'mg/l', 'value': inf['NH4']},
        {'name': 'Mn', 'units': 'mg/l', 'value': inf['Mn']},
      ]
    }
      
      return resp


    }


  },
  computed: {
    params() {
        return this.config.parameters
      },
    headers() {
      return this.$runtime.designState.names
    },
    steps() {
      return this.$runtime.designState.steps
    },
    values() {
      return this.$runtime.designState.values
    },
    names() {
      return this.$runtime.designState.names
    },
    influentData() {
      return this.resultSet('Influent')
    },


  }
}


</script>
<style>

#sandfilter-design {
  min-height: 800px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
}
#sandfilter-process {
  position: relative;
  margin: auto;
  width: 1000px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center 
}
#sandfilter-process[doublelayer="true"] {
  background: url('./assets/process-double.png') no-repeat center
}
#sandfilter-process[doublelayer="false"][sprayer="true"] {
  background: url('./assets/process-spray.png') no-repeat center
}
#sandfilter-process[doublelayer="true"][sprayer="true"] {
  background: url('./assets/process-spray-double.png') no-repeat center
}
#sandfilter-process .spray{ 
  margin: 10px;
}

#sandfilter-design .influent {
  top: 50%;
  left: 4px;
}

#sandfilter-table {
  position: absolute;
  top: 10px;
  right: -35px;
  border-collapse: collapse;
  border-spacing: 0;
  font-size: 13px;
  text-align: center;
}
#sandfilter-table tr td:first-child {
  font-weight: bold;
  text-align: left;
  padding-right: 10px;
}
#sandfilter-table td {
  padding: 5px;
}
#sandfilter-table td {
  border-bottom: 1px solid #CCC;
}
#sandfilter-design .depth-charts .result-chart {
  height: 430px;
}
#sandfilter-design .depth-charts ul {
  margin-top: 60px;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 328px;
}
#sandfilter-design .depth-charts ul li {
  text-align: right;
  list-style: none;
}
#sandfilter-design .effluent {
  right: 10%;
  bottom: 2%;
}

#sandfilter-table .warning {
  color: #F56C6C;
  font-weight: bold;
}

</style>