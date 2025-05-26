<template>
  <div class="about-dialog">
    <div class="amanzi-logo"></div>
    <div class="about-text">
      <h1>Amanzi v{{ $version }}</h1>
      <p>{{ $t('ui.dialogs.about.developed_by') }}</p>
      <p class="remark">{{ $t('ui.dialogs.about.remark') }}</p>
    </div>
    <el-collapse>
      <el-collapse-item name="changelog">
        <pre>{{ changelog }}</pre>
        <template #title><i class="fa fa-history"></i> {{ $t('ui.dialogs.about.changelog') }}</template>
      </el-collapse-item>
      <el-collapse-item name="acknowledgements">
        <pre>{{ acknowledgements }}</pre>
        <template #title><i class="fa fa-users"></i> {{ $t('ui.dialogs.about.acknowledgements') }}</template>
      </el-collapse-item>
      <el-collapse-item :title="$t('ui.dialogs.about.license')" name="license">
        <pre>{{ license }}</pre>
        <template #title><i class="fa fa-balance-scale"></i> {{ $t('ui.dialogs.about.license') }}</template>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>
<script>
import changelog from '@@/changelog.md?raw'
import acknowledgements from '@@/ACKNOWLEDGEMENTS?raw'
import license from '@@/LICENSE?raw'
export default {
  data() {
    return {
      changelog,
      acknowledgements,
      license
    }
  }
}
</script>

<style>
.about-dialog {
  width: 600px;
}
.about-text {
  padding: 20px 50px;
  text-align: center;
}
.amanzi-logo {
  width: 500px;
  margin-left: 50px;
  margin-top: 20px;
  height: 80px;
  background-image: url('@/assets/logo.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
}
.about-dialog pre {
  max-height: 500px;
  font-size: 11px;
  background-color: #f5f7fa;
  padding: 10px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  text-align: justify;
}
.about-dialog .el-collapse-item__header {
  font-size: 1.0em;
}
.about-dialog .el-collapse-item__header i {
  margin-right: 10px;
  font-size: 1.0em;
}
.remark {
  font-size: 0.9em;
  color: #666;
  text-align: justify;
}
</style>