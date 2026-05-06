<template>
  <el-scrollbar>

  <el-collapse v-model="openPanels">
    <el-collapse-item :title="$t('ui.sidebar.scenario.label')" name="scenario">
        <el-input v-model="this.$project.scenario.notes" :placeholder="$t('ui.sidebar.scenario.notes_placeholder')" type="textarea" :autosize="{ minRows: 2, maxRows: 12}" @change="this.$project.scenario.unsaved = true"/>
    </el-collapse-item>
    <el-collapse-item :title="$t('ui.sidebar.library.label')" name="library">
      <Library></Library>
    </el-collapse-item>
    <el-collapse-item :title="$t('ui.sidebar.configuration.label')" name="config">
      <Config></Config>
    </el-collapse-item>
  </el-collapse>
  </el-scrollbar>
</template>
<script>
import Library from './Library.vue'
import Config from './Config.vue'

export default {
  name: 'Sidebar',
  data() { return {
    openPanels: ['scenario', 'library', 'config'],
  }},
  methods: {
    load() {
      this.$project.open()
    },
    clear() {
      localStorage.clear()
    },
    save() {
      this.$project.save()
    },
    undo() {
      this.$project.scenario.$undo()
    },
    redo() {
      this.$project.scenario.$redo()
    }
  },

  computed: {
  },
  components: {
    Library, Config
  }
}

</script>
<style>
.el-collapse-item__header {
  padding-left: 10px !important;
  border-bottom: 1px solid #aaa;
}
.el-collapse-item__header.is-active {
  border-bottom: 1px solid #aaa;
}
.el-collapse-item__wrap {
  padding: 5px 10px;
}
</style>