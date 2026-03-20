<template>
  <div class="design-container">
    <el-container>
      <el-aside id="parameters" class="design-config">
        <ParameterInput v-model="editingModel.configuration.parameters" :type="editingModel.type" :uid="editingModel.uid"></ParameterInput>
      </el-aside>
      <el-main id="design">
        <el-tabs>
          <component :is="'design-'+editingModel.type" :config="editingModel.configuration" v-if="editingModel"></component>
        <el-tab-pane lazy>
          <template #label>
            <el-icon size="14px"><i class='fa fa-exchange'></i></el-icon><span>{{$t('ui.design.categories.massbalance')}}</span>
          </template>
          <Massbalance :modelcategory="editingModel.category"></Massbalance>
        </el-tab-pane>
        <el-tab-pane lazy>
          <template #label>
            <el-icon size="14px"><Guide /></el-icon><span>{{$t('ui.design.categories.hydraulic_line')}}</span>
          </template>
          <Hydraulicline v-if="$project.designState.hydraulics"></Hydraulicline>
        </el-tab-pane>
        <el-tab-pane lazy>
          <template #label>
            <el-icon size="14px"><i class='fa fa-table'></i></el-icon><span>{{$t('ui.design.categories.design_tables')}}</span>
          </template>
          <DesignTables></DesignTables>
        </el-tab-pane>
        </el-tabs>

      </el-main>
    </el-container>
  </div>

</template>
<script>
import ParameterInput from './ParameterInput.vue'
import DesignTables from './DesignTables.vue'
import Massbalance from './Massbalance.vue'
import Hydraulicline  from './Hydraulicline.vue'

export default {

  components: {ParameterInput, DesignTables, Massbalance, Hydraulicline},
  computed: {
    editingModel() {
      var mdl = this.$project.scenario.models.find(m => m.uid == this.$project.scenario.editingModel)
      console.log(mdl.name);
      return mdl
    }
  },
}


</script>
<style>
#design .el-tabs__item span {
  padding-left: 5px;
}
#design {
  padding: 0px 10px;
  padding-bottom: 15px;
  min-height: 80vh;
  min-width: 1000px;
}
#parameters {
}

.design-container {
  /* min-height: 80vh; */
}
.el-overlay-dialog {
  min-width: 1000px;
}
.el-dialog__body {
  padding: 0px !important;
  min-width: 1000px;
}

.el-dialog__header {
  padding: 0px !important;
  /* height: 20px; */
  border-bottom: 2px solid #CCC;
}
.design-config {
  min-width: 400px;
  /* padding: 15px; */
  padding-right: 10px;
  display: flex;
  background-color: #FCFCFC;
  border-right: 1px solid #E4E7ED;
}
.design-config .el-tab-pane .design-hydraulic {
  height: 1000px;
  width:100%;
}
.design-config .el-tabs__header {
  background: #EEE;
}
.design-config .el-tabs__item {
  width: 62px;
  height: 62px;
  padding: 0px 5px;
  align-items: center;
  flex-direction: column;
}
.design-config .el-tabs--left .el-tabs__item.is-left {
  justify-content: center;
}
.design-config .el-tabs__item i {
  display: block;
}
.design-config .el-tabs__item span {
  display: block;
  font-size: 10px;
}
.design-config .el-tabs__content {
  padding-left: 5px;
  padding-top: 10px;
  padding-bottom: 5px;
}
.design-config h3 {
  margin-top: 0px;
}
.process {
  position: relative;
}

.process .result:last-child {
  border-bottom: none;
}

</style>