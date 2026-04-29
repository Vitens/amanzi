<template>
  <el-tab-pane id="ionexchange-design">
    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
      </template>
    <!-- <el-aside id="ionexchange-config" class="design-config">
      <el-form label-position="top">
        <h3>Proces</h3>
        <el-form-item label="Aantal ionexchanges">
          <el-input type="number" :step="1" min="1">
            <template #append>
               eenheden
            </template>
          
          </el-input>
        </el-form-item>
        <el-form-item label="Nominale Capaciteit">
          <el-input type="number" :step="1" min="1">
            <template #append>
                m3/h
            </template>
          </el-input>
        </el-form-item> -->



        <!-- <el-form-item label="Recirculatiefactor">
          <el-input type="number" :step="1" min="0" max="95" v-model="config.recirculation" placeholder="0">
            <template #append>
                %
            </template>
          </el-input>
        </el-form-item> -->
        <!-- <el-form-item label="Resin capcity">
          <el-input type="number" :step="1" min="0" max="100">
            <template #append>
                -
            </template>
          </el-input>
        </el-form-item>

      </el-form>

    </el-aside> -->
    <el-main id="ionexchange-design">
      <div class="process">
        <div id="ionexchange-process" :class="{'recirculation': config.recirculation > 0}">
          <Result name="influent" color="blue" :components="resultSet('influent')" />
          <Result name="effluent" color="green" :components="resultSet('effluent')" />
        </div>
      </div>

      <el-row>
        <el-col :lg="8" :sm="12">

        </el-col>
        <el-col :lg="8" :sm="12">


        </el-col>
        <!-- <el-col :lg="8" :sm="12">
          <chart :xmin="0" :xmax="50" :datasets="oxygen" title="Zuurstof" ylabel="Volume (m3/h / Nm3/h)" xlabel="RQ [-]" :designvalue="config.rq"></chart>
        </el-col> -->
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
  computed: {
    phdata() {
      return [
        { label: 'pH', backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.output('charts', 'pH', 2, true)},
      ]
    },
    effluentData() {
      return [
        { label: 'CH4', backgroundColor: colors.green, borderColor: colors.green, radius: 0, showLine: true, data: this.output('charts', 'ch4', 2, true) },
        { label: 'CO2', backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.output('charts', 'co2', 2, true)},
        { label: 'O2', backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.output('charts', 'o2', 2, true)},
      ]
    },

  },
  methods: {
    output(group, key, precision=2, list=false) {
      // if key not in $project.designState, return '-'
      const resp = list ? [] : '-'
      if(!(group in this.$project.designState)) { return resp }
      if(!(key in this.$project.designState[group])) { return resp }

      let val = this.$project.designState[group][key]
      return list ? val : val.toFixed(precision)
    },
    resultSet(group) {
      if(!(group in this.$project.designState)) { return false }

      let data = this.$project.designState[group]

      let result = []
      for (let [key, value] of Object.entries(data)) {
        result.push({name: key, value: value, units: 'ng/l'}) // adjust this line as needed
      }
      return result
      
    },

  }
}


</script>
<style>

#ionexchange-design {
  min-height: 200px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
}
#ionexchange-process {
  position: relative;
  margin: auto;
  width: 1547px;
  height: 400px;
  background: url('./assets/process.png') no-repeat center
}
#ionexchange-process .influent {
  left: 15%;
  top: 10%;
}
#ionexchange-process .effluent {
  left: 72%;
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