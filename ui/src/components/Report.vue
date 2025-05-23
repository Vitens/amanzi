<template>
  <div id="report-container" ref="report-container">
    <el-affix :target="reportContainer" :offset="0">
      <div class="report-controls">
        <el-select v-model="scenario" placeholder="Select scenario" @change="metric_index = 0" :disabled="comparison">
          <el-option v-for="(scenario, index) in $project.reportState.scenarios" :key="index" :label="scenario" :value="index"></el-option>
        </el-select>
        <el-switch active-text="Comparison" inactive-text="Single model" v-model="comparison" class="switch-report-compact"></el-switch>
        <el-switch active-text="Compact" inactive-text="Uitgebreid" v-model="compact" class="switch-report-compact" :disabled="!comparison"></el-switch>
      </div>
    </el-affix>
    <div id="single-report" v-if="!comparison">
      <h2>{{ $t('ui.report.general.waterquality') }}</h2>
      <div class="resultset">
        <ScenarioChart namespace="quality" :scenario="scenario" :sum="false"></ScenarioChart>
        <ComparisonTable namespace="quality" :scenario="scenario" :sequential="true"></ComparisonTable>
      </div>
      <h2>{{ $t('ui.report.general.energy') }}</h2>
      <div class="resultset">
        <ScenarioChart namespace="energy" :scenario="scenario" :sum="true"></ScenarioChart>
        <ComparisonTable namespace="energy" :scenario="scenario" :sequential="false"></ComparisonTable>
      </div>
      <h2>{{ $t('ui.report.general.sustainability') }}</h2>
      <div class="resultset">
        <ScenarioChart namespace="sustainability" :scenario="scenario" :sum="true"></ScenarioChart>
        <ComparisonTable namespace="sustainability" :scenario="scenario" :sequential="false"></ComparisonTable>
      </div>

    </div>
    <div id="report-loading">
    </div>

    <div id="report" :class="{compact: compact}" v-if="comparison">
      <div class="metric">
        <h2>Kwantiteit</h2>
        <ComparisonChart namespace="quantity"></ComparisonChart>
        <ComparisonTable namespace="quantity" v-if="!compact"></ComparisonTable>
      </div>
      <div class="metric">
      <h2>Waterkwaliteit</h2>
      <ComparisonChart namespace="quality"></ComparisonChart>
      <ComparisonTable namespace="quality" v-if="!compact"></ComparisonTable>
      </div>
      <div class="metric">
      <h2>Energie</h2>
      <ComparisonChart namespace="energy"></ComparisonChart>
      <ComparisonTable namespace="energy" v-if="!compact"></ComparisonTable>
      </div>
      <div class="metric">
      <h2>Duurzaamheid</h2>
      <ComparisonChart namespace="sustainability"></ComparisonChart>
      <ComparisonTable namespace="sustainability" v-if="!compact"></ComparisonTable>
      </div>
    </div>
  </div>
</template>
<script>
import ComparisonTable from './ComparisonTable.vue'
import ComparisonChart from './ComparisonChart.vue'
import ScenarioChart from './ScenarioChart.vue'

export default {
  data() { return {
    scenario: 0,
    comparison: false,
    compact: false
  }},
  created() {
    this.scenario = this.$project.selectedScenario
  },
  watch: {
    scenario(newVal) {
      console.log("scenario changed to", newVal)
    }
  },
  components: {
    ComparisonTable,
    ComparisonChart,
    ScenarioChart
  },
  computed: {
    reportContainer() {
      return this.$refs['report-container']
    }
  }
}
</script>
<style>
#report-container {
  position: relative;
}
.report-controls {
  background-color: #EEE;
  padding-top: 10px;
  padding-left: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #AAA;
  display: flex;
}
.report-controls .el-select {
  margin-top: 5px;
  width: 300px;
}

.switch-report-compact {
  margin-top: 5px;
  margin-left: 20px;
  margin-bottom: -10px;
}
#report, #single-report {
  padding: 2px 20px;
  padding-bottom: 40px;
}
#report, #single-report h2 {
  border-bottom: 1px solid #CCC;
}
#single-report .comparison-table-container table {
  width: 100%;
}

#report .comparison-table-container {
  display: inline-block;
}

#report.compact {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

#report.compact .metric {
  width: 580px;
}

#report .compact {
  display: flex;
  flex-wrap: wrap;
}
#report .comparison-chart {
  width: 620px;
}

#report.compact .comparison-chart {
  width: 500px;
}



.result-table {
  border-spacing: 0px;
}
.result-table th {
  text-align: left;
  padding: 5px;
  border-bottom: 2px solid #AAA;
}
.result-table td {
  padding: 10px 5px;
  border-bottom: 1px solid #CCC;
}
.resultset {
  display: flex;
  flex-direction: column;
}
</style>