<template>
  <div class="design-tables">

    <el-radio-group v-model="mode" size="small">
      <el-radio-button label="tables"><i class='fa fa-table'></i></el-radio-button>
      <el-radio-button label="list"><i class='fa fa-list'></i></el-radio-button>
    </el-radio-group>
    
    <Masonry :cols="cols" v-if="mode == 'tables'">

      <div class="parameter-table" v-for="item, index in tables" :key="item.name">
        <h1>{{ $t('ui.design.tables.headers.'+item.name) }}</h1>
        <ParameterTable :table="item"></ParameterTable>
      </div>
    </Masonry>

    <ParameterList v-else></ParameterList>


  </div>
</template>
<script>

import ParameterTable from './ParameterTable.vue'
import ParameterList from './ParameterList.vue'
import Masonry from './Masonry.vue'

export default {
  data() {
    return {
      mode: 'tables',
      heights: {},
      cols: {
        'default': 1,
        1719: 1,
        2650: 2,
        3100: 3,
        3500: 4,
      }
    }
  },
  components: {
    ParameterTable,
    ParameterList,
    Masonry
  },
  computed: {
    tables() {
      if (this.$runtime.designState.tables) {
        let tables = this.$runtime.designState.tables
        tables = tables.filter(table => table.outputs.length > 0)

        return tables
      }
      return []
    },
  }
}
</script>

<style>
.design-tables {
  max-height: 83vh;
  overflow-y: auto;
}
.parameter-table {
  font-size: 13px;
  /* max-width: 680px; */
}
</style>