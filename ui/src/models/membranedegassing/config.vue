<template>
  <el-form-item label="Vacuumdiepte">
    <el-input type="number" :min="0.03" :max="1" :step="0.01" :controls="false" v-model="config.vacuum">
    
    <template #append>
      bara
    </template>
    
    </el-input>

  </el-form-item>
</template>
<script>

export default {
  name: 'config-vacuum',
  props: ['config'],
  data()  { return {
    fraction: 0
  }},
  mounted() {
  },
  watch: {
  }

}

</script>
