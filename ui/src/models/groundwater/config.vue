<template>
  <el-form-item label="Productie">
    <el-input type="number" v-model="config.production" :min="0" :max="100" :step="1">
        <template #append>
          Mm<sup>3</sup>/j
        </template> 
    
    </el-input>
  </el-form-item>
</template>

<script>
export default {
  name: 'config-groundwater',
  props: ['config']
}
</script>
<style>

</style>