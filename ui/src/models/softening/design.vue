<template>
  <el-tab-pane>

    <template #label>
      <el-icon size="14px"><i class='fa fa-bar-chart'></i></el-icon><span>Schematisch</span>
    </template>

    <div id="softening-design">
          <div class="process">
            <div id="softening-process" :class="['acid-'+params.acid_position]">
              <div class="acid-dosage">
                <div class="chemical">{{ params.acid_chemical }}</div>
                <div class="dosage">{{ parseFloat(params.acid_dosage).toFixed(2) }} mmol/l</div>
              </div>
              <div class="base-dosage">
                <div class="chemical">{{ params.base_chemical }}</div>
                <div class="dosage">{{ parseFloat(params.base_dosage).toFixed(2) }} mmol/l</div>
              </div>
              <div class="influent_flow">
                Reactor: {{ params.nominal_capacity }} m<sup>3</sup>/h
              </div>
              <div class="bypass">
                Bypass: {{ (params.bypass_open * 100) }}&percnt; ({{ (params.bypass_capacity * params.bypass_open) }} m<sup>3</sup>/h)
              </div>

              <Result name="influent" color="blue" :components="resultSet('influent')" />
              <Result name="effluent" color="green" :components="resultSet('effluent')" />
              <Result name="neutralized" color="red" :components="resultSet('neutralized')" v-if="params.acid_position != 'after-bypass' " compact />
              <Result name="mixed" color="red" :components="resultSet('mixed')" compact v-if="params.acid_position == 'after-bypass' && params.bypass > 0"/>
              <Result name="dosed" color="green" :components="resultSet('dosed')" compact/>
              <Result name="softened" color="green" :components="resultSet('softened')" compact/>
            </div>
          </div>
          <el-row>
            <el-col :lg="12" :sm="12">
              <chart :xmin="0" :datasets="phdata" :title="$t('models.softening.design.pH')" :xlabel="$t('models.softening.design.Dosering') + ' mmol/l'" :ymin2="0.5" :ymax2="1" :designvalue="params.base_dosage"></chart>
            </el-col>

            <el-col :lg="12" :sm="12">
              <chart :xmin="0" :datasets="hhdata" :title="$t('models.softening.design.Doseercurve') + ' HH'" :xlabel="$t('models.softening.design.Dosering') + ' mmol/l'" :designvalue="params.base_dosage" :ylabel="$t('models.softening.design.Hardheid') + ' [mmol/l]'"></chart>
            </el-col>

            <el-col :lg="12" :sm="12">
              <chart :xmin="0" :datasets="hco3data" :title="$t('models.softening.design.Doseercurve') + ' HCO3'" :xlabel="$t('models.softening.design.Dosering') + ' mmol/l'" :designvalue="params.base_dosage" :ylabel="$t('models.softening.design.HCO3') + ' [mg/l]'"></chart>
            </el-col>

            <el-col :lg="12" :sm="12">
              <chart :xmin="0" :datasets="scdata" :title="$t('models.softening.design.Doseercurve') + ' EGV'" :xlabel="$t('models.softening.design.Dosering') + ' mmol/l'" :designvalue="params.base_dosage" :ylabel="$t('models.softening.design.EGV') + ' [mS/cm]'  "></chart>
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
  "blue" : "#1f77b4",
  "orange" : "#ff7f0e",
  "green" : "#2ca02c",
  "red" : "#d62728",
  "purple" : "#9467bd",
  "brown" : "#8c564b",
  "pink" : "#e377c2",
  "gray" : "#7f7f7f",
  "olive" : "#bcbd22",
  "cyan" : "#17becf"
}

export default {
  components: {Chart, Result, Percent, DesignTables},
  props: ['config'],
  data() { return {
    openTab: 'Dose',
  }},
  computed: {
    params() {
      return this.config.parameters
    },
    phdata() {
      return [
        {label: this.$t('models.softening.design.Kalkmelk doseren'), backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.dataset('Ca(OH)2', 'dosed_pH')},
        {label: this.$t('models.softening.design.NaOH doseren'), backgroundColor: colors.green, borderColor: colors.green, radius: 0, showLine: true, data: this.dataset('NaOH', 'dosed_pH')},
        {label: this.$t('models.softening.design.Kalkmelk ontharden'), backgroundColor: colors.orange, borderColor: colors.orange, radius: 0, showLine: true, data: this.dataset('Ca(OH)2', 'softened_pH')},
        {label: this.$t('models.softening.design.NaOH ontharden'), backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.dataset('NaOH', 'softened_pH')},
      ]
    },
    hhdata() {
      return [
        {label: this.$t('models.softening.design.Kalkmelk'), backgroundColor: colors.blue, borderColor: colors.blue, radius: 0, showLine: true, data: this.dataset('Ca(OH)2', 'softened_hh')},
        {label: this.$t('models.softening.design.Natronloog'), backgroundColor: colors.red, borderColor: colors.red, radius: 0, showLine: true, data: this.dataset('NaOH', 'softened_hh') },
      ]
    },
    hco3data() {
      return [
        {label: this.$t('models.softening.design.Kalkmelk'), backgroundColor: colors.green, borderColor: colors.green, radius: 0, showLine: true, data: this.dataset('Ca(OH)2', 'softened_hco3')},
        {label: this.$t('models.softening.design.Natronloog'), backgroundColor: colors.orange, borderColor: colors.orange, radius: 0, showLine: true, data: this.dataset('NaOH', 'softened_hco3')},
      ]
    },
    scdata() {
      return [
        {label: this.$t('models.softening.design.Kalkmelk'), backgroundColor: colors.purple, borderColor: colors.purple, radius: 0, showLine: true, data: this.dataset('Ca(OH)2', 'softened_sc')},
        {label: this.$t('models.softening.design.Natronloog'), backgroundColor: colors.cyan, borderColor: colors.cyan, radius: 0, showLine: true, data: this.dataset('NaOH', 'softened_sc')},
      ]
    }
  },
  methods: {
    dataset(group, key) {
      if(this.$project.designState.charts == undefined) { return [] }
      if(!(group in this.$project.designState.charts)) { return [] }
      if(!(key in this.$project.designState.charts[group])) { return [] }
      return this.$project.designState.charts[group][key]
    },
    output(group, key) {
      const resp = []
      if(!(group in this.$project.designState)) { return resp }
      if(!(key in this.$project.designState[group])) { return resp }
      return this.$project.designState[group][key]
    },
    resultSet(group) {

      if(!(group in this.$project.designState)) { return [] }

      let data = this.$project.designState[group]

      let resp = [
        {name: 'pH', value: data.pH, units: '-'},
        {name: 'EGV', value: data.sc, units: 'ms/cm'},
      ]

      if(group == 'influent' || group == 'dosed') {
        resp.push({name: 'CO2', value: data.CO2, units: 'mg/l'})
      }

      if(group == "influent" || group == "effluent" || group == "softened" || group == "mixed") {
        resp.push({name: 'TH', value: data.hardness, units: 'mmol/l'})
        resp.push({name: 'HCO3', value: data.HCO3, units: 'mg/l'})
      }

      if(group == 'effluent') {
        resp.push({name: 'TACC90', value: data.ccpp90, units: 'mmol/l'})
      }

      resp.push({name: 'SI', value: data.si, units: '-'})
        

      return resp
      
    }

  }
}


</script>
<style>
#softening-design {
  min-height: 1000px;
  padding: 0px 10px;
}
.process {
  border-radius: 5px;
  width: 100%;
  border: 1px solid #CCC;
  overflow: hidden;
}
#softening-process {
  position: relative;
  margin: auto;
  width: 900px;
  height: 400px;
  background: url('./assets/process-product.png') no-repeat center
}
#softening-process.acid-bypass {
  background: url('./assets/process-bypass.png') no-repeat center
}
#softening-process.acid-after-bypass {
  background: url('./assets/process-effluent.png') no-repeat center
}
.acid-dosage, .base-dosage {
  position: absolute;
  text-align: center;
  font-size: 12px;
  width: 76px;
  padding: 1px;
  background: #EEE;
  border: 1px solid #CCC;
  border-radius: 5px;
}
.acid-dosage .chemical, .base-dosage .chemical {
  display: inline-block;
  font-weight: bold;
  padding: 1px;
}
.base-dosage {
  top: 53%;
  left: 24%;
}
.acid-bypass .acid-dosage {
  left: 24%;
  top: 73%;
}
.acid-after-bypass .acid-dosage {
  right: 20.5%;
  top: 68%;
}
.acid-reactor-outlet .acid-dosage {
  left: 61%;
  top: 38%;
}
#softening-design .influent {
  left: 2%;
  top: 57%;
}
#softening-design .effluent {
  bottom: 1%;
  right: 0%;
}
#softening-design .mixed {
  bottom: 1%;
}
#softening-design .dosed {
  left: 33.1%;
  top: 54%;
}
#softening-design .softened {
  top: 5%;
  left: 60%;
}
#softening-design .acid-reactor-outlet .neutralized {
  left: 60%;
  top: 50%;
}
#softening-design .acid-bypass .neutralized {
  left: 33.1%;
  bottom: 6%;
}
#softening-design .acid-bypass .effluent, #softening-design .acid-reactor-outlet .effluent {
  right: 5%;
}
#softening-design .mixed {
  left: 60%;
  bottom: 6%;
}
#softening-design .bypass {
  position: absolute;
  bottom: 7%;
  left: 45%;
}

#softening-design .tabs .el-tab-pane {
  min-height: 1000px;
}
#softening-design .bypass sup {
  font-size: 9px;
}
#softening-design .influent_flow {
  position: absolute;
  top: 150px;
  left: 260px;
}
#softening-design .influent_flow sup {
  font-size: 9px;
}

</style>