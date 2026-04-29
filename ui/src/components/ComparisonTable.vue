<template>

<div class="comparison-table-container">
  <copy-button :target="'.comparison-table.'+namespace"></copy-button>

  <table v-if="$project.reportState.results" class="result-table comparison-table" :class="namespace">
    <colgroup span="1" />
    <colgroup :span="columns.length" class="comparison-scenarios" />
    <colgroup span="1" />
    <thead>
      <th></th>
      <th v-for="col,column_index in columns" @mouseenter="docompare(null, column_index)" @mouseleave="stopcompare(null,column_index)">{{ col }}</th>
      <th></th>
    </thead>
    <tbody>
      <tr v-for="row, row_index in metrics">
        <td>{{ $t('ui.report.'+namespace+'.metrics.'+row.name) }}</td>
        <td v-for="s, column_index in columns" @mouseenter="docompare(row_index , column_index)" @mouseout="stopcompare()"
        :class="{highlight: (compare.row === null) ? (compare.column == column_index) : (compare.row == row_index )}"
        >
          <span v-if="(compare.row === null && compare.column !== null && compare.column != column_index) || (compare.row == row_index  && compare.column != column_index)" :class="compareClass(row, row_index, column_index)" class="value-comparison">
            {{ relative(row_index ,column_index,true) }}
          </span>
          <span v-else>
            {{ format(column_index, row_index) }}
          </span>

        </td>
        <td>{{ row.uom }}</td>
      </tr>
    </tbody>
  </table>
  </div>
</template>
<script>
import CopyButton from './CopyButton.vue';

export default {
  components: {CopyButton},
  name: 'ComparisonTable',
  props: ['namespace', 'scenario', 'sequential'],
  data() { return {
    shift: false,
    compare: {
      row: null,
      column: null
    }
  }},
  mounted() {
    this.keydownevt = document.addEventListener('keydown', (e) => {
      if(e.key === 'Shift') {
        this.shift = true
      }
    })
    this.keyupevt = document.addEventListener('keyup', (e) => {
      this.shift = false
    })
  },
  unmounted() {
    document.removeEventListener('keydown', this.keydownevt)
    document.removeEventListener('keyup', this.keyupevt)
  },
  methods: {
    compareClass(row, row_index, column_index) {
      if((this.scenario !== undefined && column_index==0) || (Math.abs(this.relative(row_index, column_index)) <= 1e-4)) {
        return ''
      }
      if ((row.positive && this.relative(row_index ,column_index)<0) || (!row.positive && this.relative(row_index ,column_index)>0)) {
        return 'negative'
      } else {
        return 'positive'
      }
    },
    relative(row_index , column_index, string) {

      let value = this.values[row_index ][column_index]

      var compare

      if(this.sequential) {
        if(column_index === 0) {
          return this.format(column_index, row_index)
        } else {
          compare = this.values[row_index ][column_index - 1]
        }
      } else {
        // compare with
        compare = this.compare.row === null ? this.values[row_index ][this.compare.column] : this.values[this.compare.row][this.compare.column]
      }

      // calculate relative difference
      var difference = (value - compare) / compare * 100


      if (string) {
        if(this.shift) {
          return (difference > 0 ? "+" : "") + (value - compare).toFixed(this.metrics[row_index].precision)
        }


        if (difference > 10000) {
          return '-'
        }
        return (difference > 0 ? "+" : "") + difference.toFixed(1) + '%'
      }
      // actual value
      return difference
    },
    stopcompare() {
      this.compare.row = null
      this.compare.column = null
    },
    docompare(row_index , column_index) {
      this.compare.row = row_index 
      this.compare.column = column_index
    },
    format(column_index, row_index) {
      var si = this.scenario !== undefined ? this.scenario : 0
      // var row = this.$project.reportState.results[si].summaries[this.namespace].metrics[row_index]
      var row = this.metrics[row_index]
      if (row.value == null) { return '' }
      return this.values[row_index][column_index].toFixed(row.precision)
    }
  },
  computed: {
    columns() {
      if(this.scenario !== undefined) {
        return this.$project.reportState.results[this.scenario].summaries[this.namespace].names
      }
      return this.$project.reportState.scenarios
    },
    metrics() {
      if(this.scenario === undefined) {
        return this.$project.reportState.results[0].summaries[this.namespace].metrics
      }
      return this.$project.reportState.results[this.scenario].summaries[this.namespace].models[0]
    },
    values() {

      if(this.scenario !== undefined) {
        var outer = []
        for(var i = 0; i < this.columns.length; i++) {
          var inner = []
          for(var r of this.$project.reportState.results[this.scenario].summaries[this.namespace].models[i]) {
            inner.push(r.value)
          }
          outer.push(inner)
        }
        outer = outer[0].map((col, i) => outer.map(row => row[i]))
        return outer
      }

      var outer = []
      for (var i = 0; i < this.$project.reportState.scenarios.length; i++) {
        var inner = []
        for(var r of this.$project.reportState.results[i].summaries[this.namespace].metrics) {
          inner.push(r.value)
        }
        outer.push(inner)
      }
      // transpose values
      outer = outer[0].map((col, i) => outer.map(row => row[i]))
      return outer

    }

  }
}
</script>
<style>
.comparison-table {
  min-width: 650px;
}
.comparison-table td {
  text-align: center;
}
.comparison-table th {
  cursor: cell;
  text-align: center !important;
}
.comparison-table tr td.highlight {
  background: rgb(236, 236, 236);
  font-weight: bold;
}
.comparison-table tr td:first-child {
  text-align: right;
  font-weight: bold;
  background: #FAFAFA;
  cursor: pointer;
}
.comparison-table tr td:last-child {
  text-align: left;
  color: #666;
  font-weight: normal;
  background: #FAFAFA;
  cursor: pointer;
}
.comparison-table .comparison-scenarios {
  background: #fff;
  width: 100px;
}
.comparison-table tr td {
  cursor: cell;
}
.comparison-table tr td span {
  pointer-events: none;
}
.comparison-table .value-comparison.positive {
  color: green;
}
.comparison-table .value-comparison.negative {
  color: red;
}
.comparison-table-container {
  position: relative;
}
.comparison-table-container .copy-button {
  position: absolute;
  top: 2px;
  right: 0px;
}

</style>