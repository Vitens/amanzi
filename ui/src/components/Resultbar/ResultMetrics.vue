<template>
  <div :id="namespace" class="quickresult">
    <copy-button :target="'#' + namespace + ' table'"></copy-button>
    <h1><i class='fa' :class="icon(namespace)"></i>{{ $t('ui.sidebar.' + namespace + '.label') }}</h1>
    <table>
      <tr v-for="metric in metrics">
        <td v-if="!metric.skip_name" :rowspan="metric.rowspan ? metric.rowspan : 1">{{ $t('ui.sidebar.' + namespace + '.' + metric.name) }}</td>
        <td v-else style="display: none;"></td>
        <td :class="color(metric)">{{ output(metric) }}</td>
        <td class="units" v-html="formatUnits(metric.uom)"></td>
      </tr>
    </table>
  </div>
</template>
<script>
import CopyButton from '@/components/CopyButton.vue';

export default {
  props: ['namespace'],
  components: { CopyButton },
  methods: {
    output(metric) {
      return metric.value.toFixed(metric.precision)
    },
    icon(namespace) {
      return {
        'quantity': 'fa-tint',
        'energy': 'fa-bolt',
        'quality': 'fa-flask',
        'sustainability': 'fa-leaf'
      }[namespace]

    },
    color(metric) {
      if (metric.color) {
        return metric.color
      }
      return ''
    },
    formatUnits(uom) {
      if (uom == undefined) return '';

      // Regular expression to detect chemical formulas (e.g., CO2, H2O, CH4)
      const chemicalRegex = /([A-Z][a-z]*)(\d*)/g;

      // Regular expression to detect metric units with superscript (e.g., m3, km2)
      const metricRegex = /([a-zA-Z]+)(\d+)/g;

      // Replace chemical formulas with subscripts for numbers
      uom = uom.replace(chemicalRegex, (match, element, number) => {
        return element + (number ? `<sub>${number}</sub>` : '');
      });

      // Replace metric units with superscripts for numbers
      uom = uom.replace(metricRegex, (match, unit, power) => {
        return `${unit}<sup>${power}</sup>`;
      });

      return uom;
    },
  },
  computed: {
    metrics() {
      if (!this.$project.state.metrics) { return [] }

      var metrics = this.$project.state.metrics[this.namespace]

      for(var i=0; i<metrics.length; i++) {

        let metric = metrics[i]

        if(metric.group === undefined || metric.skip_name) {
          continue
        }
        var rowspan = 1
        // count the number of rows in the group
        for(let ii = i+1; ii < metrics.length; ii++) {
          if (metrics[ii].group == metric.group) {
            metrics[ii].skip_name = true
            rowspan+=1
          } else {
            metric.rowspan = rowspan
            break
          }
        }
        metric.rowspan = rowspan
      }

      return metrics


    }
  }
}
</script>
<style>
#quality {
  background: var(--el-color-danger-light-9);
  border-left: 3px solid var(--el-color-danger-light-5);
}
#quantity {
  background: var(--el-color-primary-light-9);
  border-left: 3px solid var(--el-color-primary-light-5);
}
#energy {
  background: var(--el-color-warning-light-9);
  border-left: 3px solid var(--el-color-warning-light-5);
}
#sustainability {
  background: var(--el-color-success-light-9);
  border-left: 3px solid var(--el-color-success-light-5);
}

.quickresult {
  width: 257px;
  position: relative;
  padding: 10px;
  padding-top: 5px;
  border-bottom: 1px solid #DDD;
}

.quickresult h1 {
  margin: 7px 0px;
}
.quickresult h1 i {
  margin-right: 10px;
}

.quickresult table {
  background: rgba(255, 255, 255, 0.7);
  width: 100%;
  border-spacing: 0px;
}
.quickresult tr td {
  font-size: 14px;
  padding: 3px 10px;
}
.quickresult table tr:first-child td {
  border-top: 1px solid #AAA;
}
.quickresult table tr td {
  border-right: 1px solid #AAA;
  border-bottom: 1px solid #AAA;
  text-align: center;
}

.quickresult table tr td:first-child {
  border-left: 1px solid #AAA;
  width: 75px;
  font-weight: bold;
  text-align: right;
  border-right: 1px solid #AAA;
  border-bottom: 1px solid #AAA;
}
.quickresult table tr td:last-child {
  text-align: left;
  width: 60px;
}

.quickresult table td.red {
  background: var(--el-color-danger-light-7);
  color: var(--el-color-danger-dark-2);
  font-weight: bold;
}
.quickresult table td.orange {
  background: var(--el-color-warning-light-7);
  color: var(--el-color-warning-dark-2);
  font-weight: bold;
}
.quickresult table td.green {
  background: var(--el-color-success-light-7);
  color: var(--el-color-success-dark-2);
  font-weight: bold;
}

.quickresult .copy-button {
  position: absolute;
  right: 10px;
  top: 10px;
}
</style>