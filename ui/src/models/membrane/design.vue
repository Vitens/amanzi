<template>
  <el-tab-pane>
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>
    <el-main id="membrane-design">
        <el-row>
          <div class="process" >
            <div id="membrane-process" :class="'stage-'+num_stages">

              <div class="membrane-component">
                <el-select v-model="selected_component" placeholder="Select a component">
                  <el-option
                    v-for="item, idx in components"
                    :key="item"
                    :label="item"
                    :value="idx">
                  </el-option>
                </el-select>
              </div>
              
              <!-- Miniscopes for stream data -->
              <MiniScope :components="stream_data(0, 'feed')" :class="'stage-1-feed'"></MiniScope>
              <template v-for="index in num_stages">
                <MiniScope :components="stream_data(index-1, 'concentrate')" :class="'stage-'+(index)+'-concentrate'"></MiniScope>
                <MiniScope :components="stream_data(index-1, 'permeate')" :class="'stage-'+(index)+'-permeate'"></MiniScope>
                <div :class="'stage-'+index+'-recovery'">{{ recovery(index) }}</div>
              </template>

              <Result name="influent" color="blue" :components="resultSet('influent')" />
              <Result name="effluent" color="green" :components="resultSet('effluent')" />
              <Result name="concentrate" color="red" :components="resultSet('concentrate')" />

            </div>
          </div>
        </el-row>
        <br />
        <el-tabs tab-position="top" type="border-card">
          <el-tab-pane>
            <template #label>
              <el-icon size="14px"><Operation /></el-icon><span>Quantity</span>
            </template>
            <el-row>
              <el-col :lg="12" :sm="12" :xl="8">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('element_results','J')" title="Flux" ylabel="Flux [L/m2/h]" xlabel="Element #" roundXticks></chart>
              </el-col>
              <el-col :lg="12" :sm="12" :xl="8">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('element_results','P_osm')" :title="$t('models.membrane.design.osmotic_pressure')" ylabel="P_osm [bar]" xlabel="Element #" roundXticks></chart>
              </el-col>
              <el-col :lg="12" :sm="12" :xl="8">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('element_results','beta')" :title="$t('models.membrane.design.beta_factor')" ylabel="Beta [-]" xlabel="Element #" roundXticks></chart>
              </el-col>
              <el-col :lg="12" :sm="12" :xl="8">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('element_results','Q_f')" :title="$t('models.membrane.design.feed_flow')" :ylabel="$t('models.membrane.design.feed_flow')+' [m3/h]'" xlabel="Element #" roundXticks></chart>
              </el-col>
              <el-col :lg="12" :sm="12" :xl="8">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('element_results', 'V_e')" :title="$t('models.membrane.design.crossflow_per_module')" :ylabel="$t('models.membrane.design.crossflow_per_module')+' [m/s]'" xlabel="Element #" roundXticks></chart>
              </el-col>
              <el-col :lg="12" :sm="12" :xl="8">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('element_results', 'DP_e')" :title="$t('models.membrane.design.headloss_per_module')" :ylabel="$t('models.membrane.design.headloss_per_module')+' [bar]'" xlabel="Element #" roundXticks></chart>
              </el-col>
            </el-row>


          </el-tab-pane>
          <el-tab-pane lazy>
            <template #label>
              <el-icon size="14px"><i class="fa fa-flask" /></el-icon><span>Supersaturation</span>
            </template>
              <el-switch v-model="saturation_mode_si" active-text="Saturation Index (SI)" inactive-text="Saturation Ration (SR)"></el-switch>
              <table class="element-table">
                <thead>
                  <tr>
                    <th>Stream</th>
                    <th v-for="phase in phases" v-html="phase"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="stage in stage_si">
                    <td>{{ stage.name }}</td>
                    <td v-for="value in stage.data">{{ value }}</td>
                  </tr>
                </tbody>
              </table>
            <el-row>
              
              <el-col :lg="12" :sm="12" v-for="phase in phases">
                <chart :xmin="1" :xmax="num_modules" :datasets="chart_data('supersaturation', phase)" :title="phase" :ylabel="saturation_mode_si ? 'SI [-]' : 'SR [-]'" xlabel="Element #" roundXticks></chart>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane lazy>
            <template #label>
              <el-icon size="14px"><i class="fa fa-table"></i></el-icon><span>Elementen</span>
            </template>
            <table class="element-table">
              <thead>
                <tr>
                  <th v-for="header in headers" v-html="format(header)"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="element in $project.designState.element_results">
                  <td v-for="value, idx in element">{{formatValue(idx, value)}}</td>
                </tr>
              </tbody>  
            </table>


          </el-tab-pane>

        </el-tabs>
    </el-main>
  </el-tab-pane>

</template>

<script>
import Chart from '@/components/Chart.vue'
import Result from '@/components/ResultBlock.vue'
import MiniScope from '@/components/MiniScope.vue'
import Percent from '@/components/Percent.vue'

const colors = [
  'rgb(255, 99, 132)',
  'rgb(75, 192, 192)',
  'rgb(54, 162, 235)'
]

export default {
  components: {Chart, Result, MiniScope, Percent},
  name: 'design-membrane',
  props: ['config'],
  data() {
    return {
      saturation_mode_si: true,
      activeTab: 'overview',
      selected_component: 2,
      loading: true,
      dialogVisible: false,
      optiflux: false,
    }
  },
  methods: {
    resultSet(stream) {
      if(!this.$project.designState.streams) { return false }
      // return first five rows
      return this.$project.designState.streams[stream].slice(0,5)
    },
    recovery(stage) {
      if(!this.stage_results || stage > this.stage_results.length) return '-'
      return "R: "+(this.stage_results[stage-1].R*100).toFixed(1) + '%'
    },
    chart_data(dataset_name, metric) {


      if(!this.$project.designState[dataset_name]) { return [] }

      var element_results = this.$project.designState[dataset_name]

      // generate chart dataset
      var datasets = []
      const colors = [
        'rgb(255, 99, 132)',
        'rgb(75, 192, 192)',
        'rgb(54, 162, 235)'
      ]

      for(var s=0; s<this.num_stages;s++) {
        let dataset = {
          label: 'Stage '+(s+1),
          backgroundColor: colors[s],
          borderColor: colors[s],
          data: [],
          showLine: true,
          fill: false,
        }
        for(var e=0; e<this.num_modules; e++) {
          let e_idx = s*this.num_modules + e
          let yval = element_results[e_idx][metric]

          if(dataset_name == 'supersaturation') {
            yval = this.saturation_mode_si ? yval : (10**yval)
          }

          dataset.data.push({x: e+1, y: yval})
        }
        datasets.push(dataset)
      }
      return datasets
    },
    stream_data(index, stream) {

      if (!this.stage_results || index > this.stage_results.length-1) return [{'label': 'Q', 'value': '-', 'uom': 'm3/h' }, {'label': 'P', 'value': '-', 'uom': 'bar' }, {'label': 'TDS', 'value': '-', 'uom': 'mg/l' }]

      let stage = this.stage_results[index]

      var Q = {'feed': stage.Q_f, 'permeate': stage.Q_p, 'concentrate': stage.Q_c}[stream]
      var P = {'feed': stage.P_f, 'permeate': stage.P_p, 'concentrate': stage.P_c}[stream]

      var dataset = [
        {'label': 'Q', 'value': Q.toFixed(0), 'uom': 'm3/h' },
        {'label': 'P', 'value': P.toFixed(1), 'uom': 'bar' },
      ]
      
      var c = stage[stream+'_quality'][this.selected_component]


      var c = {
        'label': c.name,
        'value': c.value < 100 ? c.value.toFixed(2) : c.value.toFixed(0),
        'uom': c.uom
      }


      dataset.push(c)

      return dataset
    },
    formatValue(idx, value) {
      if(idx == 'stage' || idx == 'element') { return value }
      if(value == undefined) { return '-' }
      if(value >= 100) { return value.toFixed(0) }

      return value.toFixed(2)
    },
    format(value) {
      if(value == undefined) { return '-' }
      if(value == 'beta') { return 'β'}
      // replace _xxx with subscript
      return value.replace(/_([A-z]+)/g, '<sub>$1</sub>')
    }
  },
  computed: {
    parameters() {
      return this.config.parameters
    }, 
    components() {
      if(!this.$project.designState.stage_results) { return [] }
      return this.$project.designState.stage_results[0].feed_quality.map(c => c.name)
    },
    phases() {
      if(!this.$project.designState.supersaturation) { return [] }
      let resp = []
      for(var phase in this.$project.designState.supersaturation[0]) {
        if(this.$project.designState.supersaturation[0][phase] > -999) {
          resp.push(phase)
        }
      }
      return resp
    },
    headers() {
      if(!this.$project.designState.element_results) { return [] }
      return Object.keys(this.$project.designState.element_results[0])
    },
    flux_chart() {
      if(this.$project.designState && this.$project.designState.charts) {
        return this.$project.designState.charts.flux
      }
      return []
    },
    num_stages() {
      return this.config.parameters.number_of_stages
    },
    num_modules() {
      if(this.parameters.optiflux) {
        return this.config.parameters.modules_per_vessel / 2
      }
      return this.config.parameters.modules_per_vessel
    },
    stage_results() {
      if (!this.$project.designState) return false
      return this.$project.designState.stage_results
    },
    stage_si() {
      if (!this.$project.designState.stage_results) return []

      let resp = []

      for(var stage in this.stage_results) {
        let stage_data = this.stage_results[stage].concentrate_saturation
        let row = {name: 'Stage '+(parseInt(stage)+1), data: []}
        for(var phase in stage_data) {
          if(stage_data[phase] > -999) {
            let val = this.saturation_mode_si ? stage_data[phase].toFixed(2) : (10**stage_data[phase]).toFixed(0)
            row.data.push(val)
          }
        }
        resp.push(row)
      }

      return resp

    }
  },
}


</script>
<style>
#membrane-design {
  min-height: 80vh;
}
#membrane-process {
  position: relative;
  margin-top:15px;
  margin-right:auto;
  margin-left:auto;
  margin-bottom: 15px;
  width: 800px;
  height: 400px;
}
#membrane-design .membrane-component {
  position: absolute;
  top: 0;
  left: -150px;
  width: 150px;
  text-align: center;
}
#membrane-design .stage-1 {
  background: url('./assets/1_stage.png') no-repeat center
}
#membrane-design .stage-2 {
  background: url('./assets/2_stage.png') no-repeat center
}
#membrane-design .stage-3 {
  background: url('./assets/3_stage.png') no-repeat center
}
#membrane-design .stage-1-feed {
  left: 30px;
}
#membrane-design .stage-1-concentrate {
  left: 110px;
  top: 110px;
}
#membrane-design .stage-2-concentrate {
  left: 250px;
  top: 200px;
}
#membrane-design .stage-3-concentrate {
  left: 400px;
  top: 285px;
}
#membrane-design .stage-1-permeate {
  left: 380px;
  top: 0px;
}
#membrane-design .stage-2-permeate {
  left: 520px;
  top: 100px;
}
#membrane-design .stage-3-permeate {
  left: 660px;
  top: 200px;
}

#membrane-design .influent {
  left: -50px;
  bottom: 0%;
}
#membrane-design .concentrate {
  right: -50px;
  bottom: 0%;
}
#membrane-design .effluent {
  right: -50px;
  top: 5%;
}
#membrane-design .stage-1-recovery {
  position: absolute;
  left: 240px;
  top: 55px;
  font-weight: bold;
  font-size: 12px;
}
#membrane-design .stage-2-recovery {
  position: absolute;
  left: 390px;
  top: 145px;
  font-weight: bold;
  font-size: 12px;
}
#membrane-design .stage-3-recovery {
  position: absolute;
  left: 540px;
  top: 235px;
  font-weight: bold;
  font-size: 12px;
}
#membrane-design .element-table {
  border-collapse: collapse;
  text-align: center;
}
#membrane-design .element-table th, #membrane-design .element-table td {
  text-align: center;
  padding: 8px 15px;
}
#membrane-design .element-table th {
  border-bottom: 1px solid #AAA;
}
#membrane-design .element-table tr td {
  border-bottom: 1px solid #EEE;
}
/* zebra striping */
#membrane-design .element-table tr:nth-child(odd) {
  background: #FAFAFA;
}



</style>