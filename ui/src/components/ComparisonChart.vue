<template>
  <div class="comparison-chart" :class="namespace">
    <div class="buttons">
      <template v-if="metrics.length < 5">
      <el-button size="small" :type="button_type" @click="metric_index = idx" v-for="metric,idx in metrics" :plain="idx != metric_index">{{ $t('ui.report.'+namespace+'.metrics.'+metric.name) }}</el-button>
      </template>
      <template v-else>
        <el-select size="small" v-model="metric_index" placeholder="Select a metric" style="width: 200px">
          <el-option v-for="metric,idx in metrics" :key="idx" :label="$t('ui.report.'+namespace+'.metrics.'+metric.name)" :value="idx"></el-option>
        </el-select>
      </template>
    </div>
    <table>
      <thead>
        <th>Scenario</th>
        <th>{{ $t('ui.report.'+namespace+'.metrics.'+metric.name) }} ({{ metric.uom }}, <span v-if="metric.positive">{{$t('ui.report.general.higher_better')}}</span><span v-else>{{ $t('ui.report.general.lower_better') }}</span> )</th>
      </thead>
      <tbody ref="tbody">
        <div class="hover-bar" :style="{left: hoverPosition}" v-if="compare_index != null"></div>
        <tr v-for='scenario, scenario_index in $project.reportState.scenarios' :key="scenario_index">
          <td>{{ scenario }}</td>
          <td @mouseenter="compare_index = scenario_index" @mouseleave="compare_index = null" class="score-td">
            <div class="score-bar" :style="{width: bar_width(scenario_index)}" :ref="scenario_index">
              <span class='score-value' :class="score_class(scenario_index)">{{ output(scenario_index) }}</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</template>
<script>
export default {
  props: ['namespace', 'scenario'],
  data() {
    return {
      compare_index: null,
      metric_index: 0,
    }
  },
  methods: {
    score_class(scenario_index) {

      if(this.compare_index === scenario_index || this.compare_index === null) {
        return ''
      }
      var positive = this.metric.positive
      var relative = this.relative(scenario_index)

      if(relative === 0) {
        return ''
      }

      if(positive && relative > 0 || !positive && relative < 0) {
        return 'positive'
      } else {
        return 'negative'
      }
    },
    relative(scenario_index) {
      var compare = this.all_values[this.compare_index]
      var value = this.all_values[scenario_index]
      return (value - compare) / compare * 100
    },
    output(scenario_index) {
      // if comparing, show relative difference to compare_index
      if(this.compare_index == scenario_index) {
        return '100%'
      }
      if(this.compare_index !== null) {
        var relative = this.relative(scenario_index)
        return (relative > 0 ? '+' : '') + relative.toFixed(1) + '%'
      }

      return this.all_values[scenario_index].toFixed(this.metric.precision)
    },
    bar_width(scenario_index) {
      return (this.all_values[scenario_index] / Math.max(...this.all_values) * 100) + '%'
    }
  },
  computed: {
    button_type() {
      return {'quantity': 'primary', 'energy': 'warning', 'sustainability': 'success', 'quality': 'danger'}[this.namespace]
    },
    metrics() {
      if (!this.$project.reportState.results) {
        return []
      }
      return this.$project.reportState.results[0].summaries[this.namespace].metrics
    },
    hoverPosition() {
      let tbody = this.$refs['tbody']
      let bar = this.$refs[this.compare_index][0]
      if(!bar) {
        return '0px'
      }
      // get the position of the td relative to the tbody
      var offset = bar.getBoundingClientRect().right - tbody.getBoundingClientRect().left
      return offset + 'px'

    },
    metric() {
      if(!this.$project.reportState.results) {
        return {}
      }
      return this.$project.reportState.results[0].summaries[this.namespace].metrics[this.metric_index]
    },
    all_values() {
      if(!this.$project.reportState.scenarios) {
        return []
      }
      var values = []
      for(var i = 0; i < this.$project.reportState.scenarios.length; i++) {
        values.push(this.$project.reportState.results[i].summaries[this.namespace].metrics[this.metric_index].value)
      }
      return values
    }
  }

}

</script>
<style>
.comparison-chart {
  display: inline-block;
  padding: 15px;
  background: #F6F6F6;
  border: 1px solid #DDD;
  border-radius: 5px;
}
.comparison-chart table {
  width: 100%;
  border-spacing: 0px;
}
.comparison-chart td {
  padding: 10px;
}
.comparison-chart th {
  text-align: left;
  padding: 10px;
}
.comparison-chart thead th:first-child {
  width: 100px;
  text-align: right;
}
.comparison-chart tr td:first-child {
  text-align: right;
}
.comparison-chart .score-bar {
  background-color: #AAA;
  height: 20px;
  width: 100%;
  display: block;
  position: relative;
  transition: all 0.5s;
}
.comparison-chart .score-td {
  cursor: cell;
}
.comparison-chart tbody {
  position: relative;
}

.comparison-chart .score-value {
  position: absolute;
  top: 2px;
  font-size: 13px;
  right: -60px;
  width: 55px;
  background-color: #f6f6f6;
  z-index: 2;
}
.comparison-chart .score-value.positive {
  color: green;
}
.comparison-chart .score-value.negative {
  color: red;
}

.comparison-chart tr td:last-child {
  position: relative;
  padding-right: 55px;
}
.comparison-chart tbody {
  position: relative;
}

.comparison-chart .hover-bar {
  position: absolute;
  top: 0px;
  bottom: 0px;
  border-left: 1px dashed #666;
  z-index: 1;
  pointer-events: none;
}

.comparison-chart.quantity .score-bar {
  background-color: #79bbff;
  outline: 1px solid #337ecc;
}
.comparison-chart.quantity .score-td:hover .score-bar {
  background-color: #337ecc;
}
.comparison-chart.energy .score-bar {
  background-color: #ebb563;
  outline: 1px solid #a77730;
}
.comparison-chart.energy .score-td:hover .score-bar {
  background-color: #a77730;
}
.comparison-chart.sustainability .score-bar {
  background-color: #85ce61;
  outline: 1px solid #4e8e2f;
}
.comparison-chart.sustainability .score-td:hover .score-bar {
  background-color: #4e8e2f;
}
.comparison-chart.quality .score-bar {
  background-color: #F56C6C;
  outline: 1px solid #b25252;
}
.comparison-chart.quality .score-td:hover .score-bar {
  background-color: #b25252;
}
.comparison-chart.quality .el-select__wrapper {
  background: #FEF0F0;
  box-shadow: 0 0 0 1px var(--el-color-danger-light-5);
}
.comparison-chart.quality .el-select__placeholder {
  color: var(--el-color-danger);
}

</style>