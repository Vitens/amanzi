<template>
  <div class='scenario-chart' :class="namespace">
    <div class="buttons">
      <el-radio-group v-model="waterfall" size="small" class="waterfall-toggle">
        <el-radio-button :value="false"><i class='fa fa-bar-chart'></i></el-radio-button>
        <el-radio-button :value="true"><i class='fa fa-align-center'></i></el-radio-button>
      </el-radio-group>



      <template v-if="metrics.length < 5">
      <el-button size="small" :type="button_type" @click="metric_index = idx" v-for="metric,idx in metrics" :plain="idx != metric_index">{{ $t('ui.report.'+namespace+'.metrics.'+metric.name) }}</el-button>
      </template>
      <template v-else>
        <el-select size="small" v-model="metric_index" placeholder="Select a metric" style="width: 200px">
          <el-option v-for="metric,idx in metrics" :key="idx" :label="$t('ui.report.'+namespace+'.metrics.'+metric.name)" :value="idx"></el-option>
        </el-select>
      </template>

  <el-select v-model="path_index" v-if="!sum" size="small" placeholder="Select a path" style="width: 90%; margin-left: 10px;">
    <el-option v-for="path, idx in paths" :key="path.map(m => m.uid).join('-')"
      :label="path.map(m => m.name).join(' → ')" :value="idx">
    </el-option>
  </el-select>

    </div>

    <table v-if="$project.reportState.results">
      <tr class="bars">
        <td v-for="model, model_index in columns">
          <div class="zero-line" :style="{bottom: zero + '%'}"></div>
          <div class="score-bar" :style="bar_style(model_index)" :class="bar_class(model_index)">
            <span class='score-value'>{{ bar_value(model_index) }}</span>
          </div>
        </td>
      </tr>
      <tr class="models">
        <td v-for="model, model_index in columns"><span>{{ model }}</span></td>
      </tr>
    </table>
  </div>
</template>
<script>
export default {
  props: ['namespace', 'scenario', 'sum'],
  data() {
    return {
      metric_index: 0,
      path_index: 0,
      waterfall: false,
    }
  },
  watch: {
    scenario(newVal) {
      this.path_index = 0
    }
  },
  methods: {
    bar_class(model_index) {
      if(!this.waterfall) {
        return ''
      }
      if(model_index === 0) {
        return 'initial'
      }
      if(model_index === this.columns.length - 1) {
        return 'initial'
      }
      // if(this.sum) {
        // return 'positive'
      // }
      let prev, cur
      if(!this.sum) {
        prev = this.values[model_index - 1].value
        cur = this.values[model_index].value
      } else {
        cur = this.cumsum[model_index - 1]
        prev = this.cumsum[model_index]
      }
      let diff = Math.abs(prev.value - cur.value)

      if(diff < Math.pow(10, -1)) {
        return 'initial'
      }

      if(prev > cur) {
        return this.sum ? 'positive' : 'negative'
      } else {
        return this.sum ? 'negative' : 'positive'
      }
    },
    bar_style(model_index) {

      var bottom, height

      if(!this.waterfall) {
        let val = this.values[model_index]
        // min-max scaling
        height = this.scale(val.value)
        bottom = val.value >= 0 ? this.zero : this.zero-height

      } else {
        // if in waterfall mode, calculate the height and bottom based on the previous model
        // if index = 0, set bottom to 0
        if(model_index === 0) {
          height = this.scale(this.values[model_index].value, this.sum)
          bottom = this.zero
        }
        // if index = last, set bottom to 0 and height to cumsum
        else if (model_index === this.values.length - 1 && this.sum) {
          let csum = this.cumsum[model_index]
          height = this.scale(this.cumsum[model_index], this.sum)
          bottom = csum >= 0 ? this.zero : this.zero - height
        }
        else if(model_index === this.values.length - 1) {
          height = this.scale(this.values[model_index].value)
          bottom = this.zero
        }
        
        else {
          let prev = this.values[model_index - 1]
          let cur = this.values[model_index]

          if(!this.sum) { 
            // height is (absolute) difference between the two
            height = Math.abs(this.scale(cur.value) - this.scale(prev.value))
            // if the previous value is lower, set the bottom to the previous value
            if(prev.value < cur.value) {
              bottom = this.scale(prev.value)
            } else {
              // else, set the bottom to the current value
              bottom = this.scale(cur.value)
            }
          } else {
            let prev = this.cumsum[model_index - 1]
            let cur = this.cumsum[model_index]
            let diff = this.values[model_index].value

            height = this.scale(diff, true)
            
            if(diff >= 0) {
              bottom = this.zero > 0 ? this.zero - this.scale(prev, true) : this.scale(prev, true)
            } else {
              bottom = this.zero > 0 ? this.zero - this.scale(cur, true) : this.scale(cur, true)
            }

          }
        }
      }


      return {
        'height': height + '%',
        'bottom': bottom + '%',
        'width': '50px',
      }
    },
    bar_value(model_index) {
      if(this.waterfall && model_index === this.columns.length - 1) {
        if(this.sum) {
          return this.cumsum[model_index].toFixed(this.values[0].precision)
        }
      }
      let val = this.values[model_index]
      return val.value.toFixed(val.precision)
    },
    scale(val, sum) {

      let min, max

      if(sum) {
        min = Math.min(0, Math.min(...this.cumsum))
        max = Math.max(...this.cumsum)
      } else {
        min = Math.min(...this.values.map(v => v.value))
        max = Math.max(...this.values.map(v => v.value))
      }

      // If min and max are equal, return a constant scale value
      if(min === max) {
        return 50
      }

      let offset = (sum || min == 0) ? 0 : 20
      let scale = 80 - offset

      if (min >= 0) {
        return offset + (val - min) / (max - min) * scale
      } else {
        const range = max - min
        const scaledValue = Math.abs(val) / range
        return 0 + scale * scaledValue
      }


    }


  },
  computed: {
    paths() {
      if (!this.$project.scenario) return []
      // Convert model UIDs to names in each path
      if (!this.$project.reportState.results) return []
      console.log("computing paths for scenario", this.scenario)
      return this.$project.scenarios[this.scenario].findAllProductPaths()
    },
    zero() {
      let min, max

      if(this.waterfall) {
        min = Math.min(...this.cumsum)
        max = Math.max(...this.cumsum)
      } else {
        min = Math.min(...this.values.map(v => v.value))
        max = Math.max(...this.values.map(v => v.value))
      }
      if (min >= 0) {
        return 0
      }
      
      let zero = this.scale(min, this.waterfall)
      zero += this.waterfall ? 10 : 0
      return zero
    },
    button_type() {
      return {'quantity': 'primary', 'energy': 'warning', 'sustainability': 'success', 'quality': 'danger'}[this.namespace]
    },
    columns() {
      if(!this.sum) {
        return this.paths[this.path_index].map(n => n.name)
      }
      var order = this.$project.reportState.results[this.scenario].summaries[this.namespace].names
      if(this.sum && this.waterfall) {
        return order.concat('Total')
      }
      return order
    },
    values() {
      let values = []

      if(!this.sum) {
        let path = this.$project.scenarios[this.scenario].findAllProductPaths()[this.path_index]
        for(var model of path) {
          // find the index of the model in the order
          let m = this.$project.reportState.results[this.scenario].summaries[this.namespace].order.indexOf(model.uid)
          let val = this.$project.reportState.results[this.scenario].summaries[this.namespace].models[m][this.metric_index]
          // round to precision of the metric
          val.value = _.round(val.value, val.precision)

          values.push(val)
        }
      }
      else {
        for(var model of this.$project.reportState.results[this.scenario].summaries[this.namespace].models) {
          values.push(model[this.metric_index])
        }
      }

      if(this.sum && this.waterfall) {
        values.push({'value': 0, 'precision': 0})
      }
      return values
    },
    cumsum() {
      let sum = 0;
      let cumsum = []
      for(var val of this.values) {
        sum += val.value
        cumsum.push(sum)
      }
      return cumsum
    },
    metrics() {
      if (!this.$project.reportState.results) {
        return []
      }
      return this.$project.reportState.results[this.scenario].summaries[this.namespace].models[0]
    },
  }

}
</script>
<style>
.scenario-chart {
  display: inline-block;
  padding: 0px 15px;
  padding-top: 15px;
  border: 1px solid #DDD;
  border-radius: 5px;
  margin-bottom: 20px;
}
.scenario-chart .buttons {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 0px;
  margin-bottom: 15px;
}
.scenario-chart .waterfall-toggle {
  margin-right: 20px;
  width: 100px;
}
.scenario-chart table {
  margin: auto;
}
.scenario-chart .bars {
  height: 200px;
  background: white;
}
.scenario-chart .bars td:first-child {
  border-left: 1px solid #DDD;
}

.scenario-chart table {
  border-spacing: 0;
}
.scenario-chart .models td {
  min-width: 50px;
  max-width: 100px;
  height: 80px;
  padding: 5px 0px;
  font-size: 12px;
  font-weight: bold;
  position: relative;
}
/* .scenario-chart .models td::after {
  position: absolute;
  content: '';
  width: 100px;
  height: 1px;
  background: #EFEFEF;
  transform: rotate(-45deg);
  translate: 14px -20px;
} */

.scenario-chart .models td span {
  display: inline-block;
  text-align: right;
  transform: rotate(-45deg);
  width: 110px;
  overflow: hidden;
  text-overflow: ellipsis;
  transform-origin: center;
  translate: -40px 2px;
  text-wrap: nowrap;
}

.scenario-chart .bars td {
  position: relative;
  /* border-bottom: 1px solid #666; */
  border-right: 1px solid #DDD;
}
.scenario-chart .score-bar {
  position: absolute;
  bottom: 0px;
  left: 50%;
  margin-left: -25px;
  background-color: var(--el-color-primary);
  border: 1px solid var(--el-color-primary-dark-2);
  border-bottom: none;
  transition: all 0.5s;
}

.scenario-chart.energy .score-bar {
  background-color: var(--el-color-warning);
  border: 1px solid var(--el-color-warning-dark-2);
}
.scenario-chart.quality .score-bar {
  background-color: var(--el-color-danger);
  border: 1px solid var(--el-color-danger-dark-2);
}
.scenario-chart.sustainability .score-bar {
  background-color: var(--el-color-success);
  border: 1px solid var(--el-color-success-dark-2);
}

.scenario-chart .score-value {
  position: absolute;
  top: -20px;
  text-align: center;
  width: 50px;
  font-size: 12px;
  color: #666;
}

.scenario-chart .initial {
  background-color: var(--el-color-info-light-7) !important;
  border: 1px solid var(--el-color-info-dark-2) !important;
  border-bottom: none !important;
}
.scenario-chart .positive {
  background-color: var(--el-color-success) !important;
  border: 1px solid var(--el-color-success-dark-2) !important;
}
.scenario-chart .negative {
  background-color: var(--el-color-danger) !important;
  border: 1px solid var(--el-color-danger-dark-2) !important;
}

.scenario-chart .negative .score-value {
  top: unset;
  bottom: -20px;
}

.scenario-chart .initial::after, .scenario-chart .positive::after, .scenario-chart .negative::after {
  content: '';
  position: absolute;
  width: 50px;
  top: -1px;
  height: 0px;
  border-top: 1px dashed #666;
  transition: all 0.5s;
  right: -50px;
}
.scenario-chart .negative::after {
  top: unset;
  bottom: -1px;
}

.scenario-chart .bars td:last-child .score-bar::after {
  display: none;
}
.scenario-chart .bars {
  transform: scale(1);
}

.scenario-chart .zero-line {
  position: absolute;
  left: -1px;
  right: -1px;
  height: 1px;
  background-color: #666;
  z-index: 0;
}

</style>