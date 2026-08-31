<template>
  <div class="result-chart">
    <canvas ref="chart">
    </canvas>
  </div>

</template>
<script>

import Chart from 'chart.js/auto'

const vline = {
  beforeDraw(chart) {

    var xScale = chart.scales[chart.getDatasetMeta(0).xAxisID];
    var yScale = chart.scales[chart.getDatasetMeta(0).yAxisID];

    if(xScale == undefined || yScale == undefined) return


    chart.ctx.beginPath();
    // tab:red color
    chart.ctx.strokeStyle = 'red';
    chart.ctx.lineWidth = 2;
    // make dashed line
    chart.ctx.setLineDash([5, 5]);
    chart.ctx.moveTo(xScale.getPixelForValue(chart.options.plugins.vline.value), yScale.getPixelForValue(yScale.min));
    chart.ctx.lineTo(xScale.getPixelForValue(chart.options.plugins.vline.value), yScale.getPixelForValue(yScale.max));
    chart.ctx.stroke();
    chart.ctx.closePath();
    chart.ctx.setLineDash([]);
  }
}

const hline = {
  afterDraw(chart) {

    var xScale = chart.scales[chart.getDatasetMeta(0).xAxisID];
    var yScale = chart.scales[chart.getDatasetMeta(0).yAxisID];

    if(xScale == undefined || yScale == undefined) return

    if (chart.options.plugins.hline.value < yScale.min 
     && chart.options.plugins.vline.value > yScale.max) return;

    chart.ctx.beginPath();
    // tab:red color
    chart.ctx.strokeStyle = 'red';
    chart.ctx.lineWidth = 2;
    // make dashed line
    chart.ctx.setLineDash([5, 5]);
    chart.ctx.moveTo(xScale.getPixelForValue(xScale.min), yScale.getPixelForValue(chart.options.plugins.hline.value));
    chart.ctx.lineTo(xScale.getPixelForValue(xScale.max), yScale.getPixelForValue(chart.options.plugins.hline.value));
    chart.ctx.stroke();
    chart.ctx.closePath();
    chart.ctx.setLineDash([]);
  }
}

export default {
  props: {
  datasets: Array,
  xtype: {
    type: String,
    default: 'linear'
  },
  ytype: {
    type: String,
    default: 'linear'
  },
  xlabel: String,
  xlabel2: String,
  ylabel: String,
  ylabel2: String,
  title: String,
  xmin: Number,
  xmax: Number,
  ymin: Number,
  ymax: Number,
  ymin2: Number,
  ymax2: Number,
  xmin2: Number,
  xmax2: Number,
  x1x2ratio: Number,
  designvalue: Number,
  targetvalue: Number,
  subtitle: String,
  hline: Boolean,
  aspectRatio: Number,
  roundXticks: Boolean,
  reverseaxis2:{ type: Boolean,
    default: false
  }
},
  //['datasets', 'xlabel', 'ylabel', 'ylabel2', 'title', 'xmin', 'xmax', 'ymin', 'ymax', 'ymin2', 'ymax2', 'designvalue', 'targetvalue', 'subtitle', 'hline', 'aspectRatio', 'roundXticks'],


  mounted() {
    this.chart = new Chart(this.$refs.chart, this.options)
  },
  watch: {
    options() {
      this.update()
    }
  },

  computed: {
    subtitleObject() {
      return {
        display: this.subtitle != null,
        text: this.subtitle
      }
    },
    hasSecondXAxis() {
      return this.xlabel2 != null && this.x1x2ratio != null && this.x1x2ratio !== 0
    },
    x2Min() {
      if (!this.hasSecondXAxis) return undefined
      if (this.xmin2 != null) return this.xmin2
      if (this.xmin != null) return this.xmin * this.x1x2ratio
      return undefined
    },
    x2Max() {
      if (!this.hasSecondXAxis) return undefined
      if (this.xmax2 != null) return this.xmax2
      if (this.xmax != null) return this.xmax * this.x1x2ratio
      return undefined
    },
    options() {
      console.log(this.targetvalue)
      const x1x2ratio = this.x1x2ratio
      const roundXticks = this.roundXticks
      let options = {
        plugins: [vline, hline],
        type: 'scatter',
        data: {
          datasets: this.datasets
        },
        options: {
          // aspectRatio: this.aspectRatio ? this.aspectRatio : 1.66,  // 2 is default value
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            subtitle: this.subtitleObject,       
            vline: {
              value: this.designvalue
            },
            hline: {
              value: this.targetvalue 
            },
            title: {
              display: this.title != '',
              text: this.title
            },
            legend: {
              position: 'top',
              font: {size: 10}
            },
          },
          scales: {
            x: {
              ticks: {
                callback: function (value) {
                  if (this.roundXticks) {
                    return value.toFixed(0);
                  }
                  return value;
                }.bind(this),
                reverse: true,
                stepSize: this.roundXticks ? 1 : undefined,
                maxTicksLimit: this.roundXticks ? 10 : undefined,
              },
              type: this.xtype,
              position: 'bottom',
              title: {
                display: true,
                text: this.xlabel
              },
              suggestedMin: this.xmin,
              max: this.xmax
            },
            x2: {
              type: this.xtype,
              position: 'top',
              display: this.hasSecondXAxis,
              title: {
                display: true,
                text: this.xlabel2
              },
              min: this.x2Min,
              max: this.x2Max,
              grid: {
                drawOnChartArea: false
              },
              ticks: {
                reverse: true,
                callback: function (value) {
                  if (roundXticks) {
                    return value.toFixed(0)
                  }
                  return value
                },
                stepSize: roundXticks ? 1 : undefined,
                maxTicksLimit: roundXticks ? 10 : undefined,
                afterBuildTicks: (axis) => {
                  const xAxis = axis.chart.scales.x
                  if (!xAxis?.ticks?.length) return
                  axis.ticks = xAxis.ticks.map((tick) => ({
                    value: tick.value * x1x2ratio
                  }))
                }
              }
            },
            y: {
              type: this.ytype,
              position: 'left',
              title: {
                display: true,
                text: this.ylabel
              },
              min: this.ymin,
              suggestedMax: this.ymax > this.hline ? this.ymax : this.hline + 0.05
            },
            y2: {
              type: 'linear',
              position: 'right',
              title: {
                display: true,
                text: this.ylabel2
              },
              reverse: this.reverseaxis2, 
              display: this.ylabel2 != null,
              grid: {
                drawOnChartArea: false
              },
              suggestedMin: this.ymin2,
              suggestedMax: this.ymax2
            }
          }

        }
      }
    return options
  }


  },

  methods: {
    update() {
      if (!this.chart) return
      this.chart.options = this.options.options
      this.chart.data.datasets = this.datasets
      this.chart.update('none')
    }
  }
}

</script>
<style>
.result-chart {
  min-height: 300px;
}

</style>