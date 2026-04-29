<template>
  <div class="design-header">
      <span class="design-header-text">{{ model.name }}</span>
      <el-button type="primary" @click="selectModel(upstreamModels.uids[0])" v-if="upstreamModels.uids.length === 1"><el-icon class="el-icon--left"><ArrowLeft /></el-icon>{{ upstreamModels.names[0] }}</el-button>
      <el-dropdown type="primary" v-else-if="upstreamModels.uids.length > 1" trigger="hover" @click="selectModel(upstreamModels.uids[0])" split-button>
        <el-icon class="el-icon--left"><ArrowLeft /></el-icon>{{ upstreamModels.names[0] }}
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item v-for="(name, i) in upstreamModels.names" :key="upstreamModels.uids[i]" @click="selectModel(upstreamModels.uids[i])">{{ name }}</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <el-button type="primary" @click="selectModel(downstreamModels.uids[0])" v-if="downstreamModels.uids.length === 1">{{ downstreamModels.names[0] }}<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
      <el-dropdown v-else-if="downstreamModels.uids.length > 1" trigger="click" @click="selectModel(downstreamModels.uids[0])" split-button type="primary">
        {{ downstreamModels.names[0] }}<el-icon class="el-icon--right"><ArrowRight /></el-icon>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item v-for="(name, i) in downstreamModels.names" :key="downstreamModels.uids[i]" @click="selectModel(downstreamModels.uids[i])">{{ name }}</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
  </div>
</template>
<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    }
  },
  name: 'DesignHeader',
  methods: {
    async selectModel(uid) {
      // deselect current model
      this.$project.scenario.deselectBlocks();
      this.$bus.emit('selection-changed');
      // clear designstate
      this.$runtime.designState = {};
      // set new model as editing model and selected block
      this.$project.scenario.editingModel = uid;

      this.$project.scenario.selectedBlocks = [uid];
      this.$bus.emit('selection-changed');
    }
  },
  computed: {
    upstreamModels() {
      // get the models that are directly upstream of the current model
      let cons = this.$project.scenario.connections.filter(c => c.tgt === this.model.uid && c.type == 'product');
      let uids = cons.map(c => c.src);
      // get model names
      let names = uids.map(uid => this.$project.scenario.models.find(m => m.uid === uid).name);
      return {uids, names}
    },
    downstreamModels() {
      // get the models that are directly downstream of the current model
      let cons = this.$project.scenario.connections.filter(c => c.src === this.model.uid && c.type == 'product');
      let uids = cons.map(c => c.tgt);
      let names = uids.map(uid => this.$project.scenario.models.find(m => m.uid === uid).name);
      return {uids, names}
    },
    model() {
      return this.$project.scenario.models.find(m => m.uid === this.$project.scenario.editingModel);
    }

  }
}
</script>
<style>
.design-header {
  display: flex;
  justify-content: left;
  align-items: center;
  padding-right: 30px;
  height: 30px;
}
.design-header-text {
  font-size: 18px;
  font-weight: normal;
  width: 200px;
}
</style>