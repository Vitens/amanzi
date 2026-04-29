<template>
  <table class="parameter-list">
    <thead>
      <tr>
        <th>{{ $t('ui.design.parameterlist.parameter') }}</th>
        <th>{{ $t('ui.design.parameterlist.tag') }}</th>
        <th>{{ $t('ui.design.parameterlist.value') }}</th>
        <th>{{ $t('ui.design.parameterlist.units') }}</th>
        <th>{{ $t('ui.design.parameterlist.equation') }}</th>
        <th>{{ $t('ui.design.parameterlist.category') }}</th>
        <th>{{ $t('ui.design.parameterlist.section') }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="output in outputs" :key="output.uid">
        <td>{{ $t('models.'+output.namespace+'.outputs.'+output.name) }}</td>
        <td><span class='tag' :style="{'background-color': colormap[output.order]}">{{ output.name }}</span></td>
        <td>{{ format(output) }}</td>
        <td>{{ output.uom }}</td>
        <td v-html='parseEquation(output.equation)' class="equation"></td>
        <td>{{ output.category }}</td>
        <td>{{ output.section }}</td>
      </tr>
    </tbody>

  </table>
</template>
<script>
export default {
  methods: {
    format(output) {
      if (output.value === undefined) {
        return '-'
      }
      var value = output.value
      if (typeof value === 'string') return value;
      if (typeof value === 'boolean') return value ? 'Yes' : 'No';

      let precision = output.precision ? output.precision : 2
      value = output.uom == '%' ? value * 100 : value
      
      return output.value.toFixed(precision)
    },
    parseEquation(eq) {

      eq = eq.replaceAll(/\bcapacity\b/g, 'nominal_capacity')

      // eq = eq.replace(/\b\w+\.\w+\.\w+\b/g, (match) => {
      //   return `<span class='tag'>${match}</span>`
      // })

      eq = eq.replaceAll(/\b(?:[a-zA-Z0-9_]+\.)+[a-zA-Z0-9_]+\b/g, (match) => {
        console.log(match)
        return `<span class='tag'>${match}</span>`
      })

      eq = eq.replaceAll(/(?<!<[^>]*>)\b\w+\b/g, (match) => {
        if (match in this.$project.designState.outputs) {
          var color = this.colormap[this.$project.designState.outputs[match].order]
          return `<span class='tag' style="background-color: ${color};">${match}</span>`
        }
        if (match in this.$project.designState.parameters) {
          return `<span class='parameter'>${match}</span>`
        }
        return match
      })


      return eq
      

    },
    pseudoRandom(i) {
      // return a random number between 100 and 255
      // return Math.floor(Math.random() * 155) + 100

      return (i*123*(i << 12345*i) / 1234) % 155 + 150
    }
  },
  computed: {
    colormap() {
      let cmap = []
      for(var i=0; i<this.outputs.length; i++) {

        var r = Math.floor(this.pseudoRandom(i))
        var g = Math.floor(this.pseudoRandom(i+1))
        var b = Math.floor(this.pseudoRandom(i+2))
        cmap.push(`rgba(${r},${g},${b}, 0.5)`)
      }
      return cmap
    },
    outputs() {
      if(!this.$project.designState.outputs) { return [] }

      var resp = Object.keys(this.$project.designState.outputs).map(key => ({
        name: key,
        ...this.$project.designState.outputs[key]
      }))

      return resp

    }
  }
}


</script>
<style>
.parameter-list {
  margin-top: 10px;
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  color: #333;
}
.parameter-list th {
  background-color: #f0f0f0;
  border-bottom: 1px solid #CCC;
  padding: 5px;
  text-align: left;
}
.parameter-list td {
  border-bottom: 1px solid #CCC;
  padding: 5px;
}
.parameter-list .tag, .parameter-list .parameter {
  padding: 1px 5px;
  border-radius: 5px;
  font-size: 12px;
  color: #333;
  font-weight: bold;
  display: inline-block;
  margin: 0px 2px;
  outline: 1px solid #888;
}
.parameter-list .parameter {
  color: white;
  background-color: var(--el-color-primary);
}
.parameter-list .equation {
  font-size: 13px;
  font-weight: bold;
}

</style>