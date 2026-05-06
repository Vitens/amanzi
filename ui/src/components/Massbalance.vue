<template>
  <template v-for="stream in streams">
    <h3>{{ stream.name }}</h3>
    <table class="massbalance">
      <thead>
        <tr>
          <th></th>
          <th>Influent</th>
          <th>Effluent</th>
          <th>𝚫</th>
          <th>%</th>
          <th></th>
        </tr>
      </thead>
      <tr v-for="row, idx in rows">
        <td>{{ $t('ui.report.quality.metrics.'+row.name) }}</td>
        <td v-for="(col) in columns(idx)">{{ format(col.value) }}</td>
        <td>{{ delta(idx).toFixed(2) }}</td>
        <td :class="{increased: delta(idx)>0, decreased: delta(idx)<0}">{{ deltaprec(idx) }}</td>
        <td>{{ row.uom }}</td>
      </tr>
    </table>
  </template>
</template>

<script>
export default {
  props: ['modelcategory'],
  computed: {
    streams() {
      if(!this.$runtime.designState.quality) { return [] }
      return ['product']

    },
    rows() {
      if(!this.$runtime.designState.quality) { return [] }

      if (this.modelcategory == 'waste') {
        let influent = this.$runtime.designState.quality.influent_waste
        return influent
      }
      else {
        let influent = this.$runtime.designState.quality.influent_product
        return influent
      }
    },
  },
  methods: {
    format(value) {
      if (value === undefined) { return '-' }
      if (value > 100) { return value.toFixed(0) }
      if (value > 10) { return value.toFixed(1) }
      return value.toFixed(2)
    },
    columns(idx) {
      if(!this.$runtime.designState.quality) { return [] }
      if (this.modelcategory == 'waste') {
        let influent = this.$runtime.designState.quality.influent_waste
        if (this.$runtime.designState.quality.effluent_waste) {
          let effluent = this.$runtime.designState.quality.effluent_waste
          return [influent[idx], effluent[idx]]
        }
        else {
          return [influent[idx]]
        }
      }
      else {
        let influent = this.$runtime.designState.quality.influent_product
        let effluent = this.$runtime.designState.quality.effluent_product
        return [influent[idx], effluent[idx]]
    }
  },
    delta(idx) {
      if (this.modelcategory == 'waste') {
        return 0
      }
      else {
        let [a,b] = this.columns(idx)
        return (b.value - a.value)
      }
    },
    deltaprec(idx) {
      if (this.modelcategory == 'waste') {
        return 0
      }
      else {
        let [a,b] = this.columns(idx)
        let diff =  (b.value - a.value) / a.value * 100
        if (diff > 1000 || diff < -1000) {
          return '-'
        }
        return (diff > 0 ? "+ " : "- ") + diff.toFixed(1).replace("-","") + '%'
      }
    }
  }
}

</script>
<style>
.massbalance {
  width: 600px;
  border-spacing: 0px;
  text-align: center;
}
.massbalance th {
  padding: 8px 10px;
  background-color: #EEE;
}
.massbalance tr td {
  padding: 8px 10px;
  border-left: 1px solid #CCC;
  border-bottom: 1px solid #CCC;
}
.massbalance tr td:first-child {
  text-align: right;
  font-weight: bold;
}
.massbalance tr td:last-child {
  width: 50px;
  text-align: right;
  border-right: 1px solid #CCC;
}
.massbalance .increased {
  background-color: #e1f3d8;
}
.massbalance .decreased {
  background-color: #fde2e2;
}
</style>