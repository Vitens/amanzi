<template>
  <div class="result-chart">
    <canvas ref="chart">
    </canvas>
  </div>

</template>
<script>

import Chart from 'chart.js/auto'
import { reduce } from 'lodash'

export default {
  props: ['datasets', 'xlabel', 'ylabel', 'ylabel2', 'title', 'xmin', 'xmax', 'ymin', 'ymax', 'ymin2', 'ymax2', 'designvalue', 'ylabels'],


  mounted() {

    this.chart = new Chart(this.$refs.chart, this.options)

  },
  watch: {
    options() {
      this.update()
    }
  },

  computed: {
    options() {
      let options = {
        type: 'scatter',
        data: {
          datasets: this.datasets
        },
        options: {
          maintainAspectRatio: false,
          interaction: {
            mode: 'nearest',
            axis: 'y',
            intersect: false
          },
          plugins: {
            title: {
              display: true,
              text: this.title
            },
            legend: {
              position: 'top',
              font: {size: 10}
            },
          },
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
              title: {
                display: true,
                text: this.xlabel
              },
              min: this.xmin,
              grace: '5%',
            },
            y: {
              grid: {
                tickColor: 'transparent'
              },
              type: 'linear',
              position: 'left',
              title: {
                display: true,
                text: this.ylabel
              },
              ticks: {
                display: false,
              }
            },
          }

        }
      }
    return options
  }


  },

  methods: {
    update() {
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