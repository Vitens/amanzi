<template>
  <el-scrollbar id="metrics">
    <ResultMetrics namespace="quality"></ResultMetrics>
    <ResultMetrics namespace="quantity"></ResultMetrics>
    <ResultMetrics namespace="energy"></ResultMetrics>
    <ResultMetrics namespace="sustainability"></ResultMetrics>
    <div class="fill"></div>
  </el-scrollbar>

</template>
<script>
import ResultMetrics from './Resultbar/ResultMetrics.vue';

export default {
  components: {
    ResultMetrics
  },
  data() {
    return {
    }
  }
}

</script>

<style>
.fill {
  border-left: 3px solid var(--el-color-info-light-5);
  flex: 1;
}
.sidebar-right .el-scrollbar__view {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>