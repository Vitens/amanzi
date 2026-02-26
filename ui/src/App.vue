<template>
<div id="main">

  <!-- design mode dialog -->
  <el-dialog :model-value="dialogVisible" @closed="closeDialog" :width="dialogWidth" top="20px" :title="dialogTitle" class="default">
    <Design v-if="designVisible"></Design>
    <Report v-if="reportVisible"></Report>
    <KeyFigures v-if="keyFiguresVisible"></KeyFigures>
    <Tutorial v-if="tutorialVisible"></Tutorial>
    <About v-if="aboutVisible"></About>
    <template #header>
      <DesignHeader v-if="designVisible" :title="dialogTitle"></DesignHeader>
    </template>
  </el-dialog>

  <el-dialog :model-value="!initialized" width="500px" :close-on-click-modal="false" :close-on-press-escape="false" :show-close="false" :align-center="true" class="init" :close-delay="750">
    <div class="init-content">
      <div class="init-title">{{$t('ui.dialogs.init.title')}}</div>
      <div class="loader" :class="{loading: progress.value < 100}"></div>
      <div class="init-progress">{{ progress.message }}</div>
      <el-progress :percentage="progress.value" :text-inside="true" :stroke-width="25" :status="progress.value < 100 ? 'active' : 'success'"></el-progress>
    </div>

  </el-dialog>

  <el-container class="container">

    <el-header class="header">
      <LoadingIndicator></LoadingIndicator>
      <Topbar></Topbar>
    </el-header>
    <el-container class="sub-container">


      <el-aside class="sidebar" :class="{hidden: !$project.sidebar.left}">
        <Sidebar></Sidebar>
      </el-aside>
      <el-container>
      <el-main class="main">
        <div id="error" v-if="$project.invalid"><i class='fa fa-warning'></i>&nbsp;{{ $t($project.invalid_message, $project.invalid_data) }}</div>
        <Canvas></Canvas>
      </el-main>
      <el-footer height="40px" class="scenarios"><Scenariobar></Scenariobar></el-footer>
      </el-container>
      <el-aside class="sidebar-right" width="280px" :class="{hidden: !$project.sidebar.right}">
        <ResultBar></ResultBar>
      </el-aside>
    </el-container>

  </el-container>
</div>
</template>

<script>
import Canvas from './components/Canvas.vue'
import Topbar from './components/Topbar.vue'
import Sidebar from './components/Sidebar.vue'
import ResultBar from './components/Resultbar.vue'
import Report from './components/Report.vue'
import Scenariobar from './components/Scenariobar.vue'
import LoadingIndicator from './components/LoadingIndicator.vue'
import Design from './components/Design.vue'
import KeyFigures from './components/KeyFigures.vue'
import components from './models/groundwater/assets/components'
import Tutorial from './components/Dialogs/Tutorial.vue'
import About from './components/Dialogs/About.vue'
import DefaultProject from './assets/Default-project.json'
import DesignHeader from './components/DesignHeader.vue'

export default {
  name: 'App',
  components: {
    Canvas, Sidebar, Scenariobar, Design, Topbar, LoadingIndicator, Report, KeyFigures, ResultBar, Tutorial, About, DesignHeader
  },
  data() { return {
    initialized: true,
    progress: {
      value: 0,
      message: 'Initializing...'
    },
    error: false,
    dialog: true,
    sidebar: {
      left: true,
      right: true
    },
    components: components
  }},
  async mounted() {
    // check if tutorial was skipped
    const tutorialSkipped = this.$cookies.get('tutorial-skip')
    if (tutorialSkipped) {
      this.$project.tutorial = false
    }
    if (this.$backend.driver == 'pyodide') {
      this.initialized = false

      const onProgress = (progress) => {
        this.progress = progress
      }

      await this.$backend.initialize(onProgress)
    }

    this.initialized = true

    this.$project.backend = this.$backend

    this.$project.open(DefaultProject, false)





    await this.$project.loadParameters()
    this.$project.solve()

    // throttle solve requests using lodash
    this.$project.$subscribe((m, s) => {
      // check if unsolved
      // suppress keys
      this.$project.changed = true
      if (this.$project.scenario.unsolved) { 
        // this.$project.state.quality = []
        this.$project.solve() 
        this.$project.scenario.unsolved = false
      }
    })
    // zoom fit
    await this.$nextTick()
    this.$bus.emit('zoomFit')

    // add onclose event to prompt user to save
    window.addEventListener('beforeunload', (e) => {
      if(this.$project.unsaved) {
        e.preventDefault()
        e.returnValue = ''
      }
    })

    this.components.micros[1].components.forEach(item => {
      if (!this.$project.scenario.metaData.customMicroComponents['PFAS'].some(existingItem => existingItem.name === item.name)) {
        this.$project.scenario.metaData.customMicroComponents['PFAS'].push({
            name: item.name,
            chemical: item.chemical,
            PEQ: item.PFOAequviliant,
            removalIEX: 0,
            removalAKF: 0,
            removalRO: 0,
            unit: 'ng/l'
            })}})
    this.components.micros[0].components.forEach(item => {
      if (!this.$project.scenario.metaData.customMicroComponents['VOC'].some(existingItem => existingItem.name === item.name)) {
        this.$project.scenario.metaData.customMicroComponents['VOC'].push({
            name: item.name,
            unit: 'mg/l'
            })}})

  },

  computed: {
    designVisible() {
      return this.$project.scenario.editingModel != null
    },
    reportVisible() {
      return this.$project.report
    },
    keyFiguresVisible() {
      return this.$project.keyfigures
    },
    tutorialVisible() {
      return this.$project.tutorial
    },
    aboutVisible() {
      return this.$project.about
    },
    dialogVisible() {
      return this.designVisible || this.reportVisible || this.keyFiguresVisible || this.tutorialVisible || this.aboutVisible
    },
    dialogTitle() {
      if (!this.dialogVisible) { return '' }
      if (this.reportVisible) { return this.$t('ui.dialogs.report.title') }
      if (this.keyFiguresVisible) { return this.$t('ui.dialogs.keyfigures.title') }
      if (this.tutorialVisible) { return this.$t('ui.dialogs.tutorial.title') }
      if (this.aboutVisible) { return this.$t('ui.dialogs.about.title') }
      return this.$project.scenario.models.filter(m => m.uid == this.$project.scenario.editingModel)[0].name
    },
    dialogWidth() {
      if(this.reportVisible) { return '1300px' }
      if(this.keyFiguresVisible) { return '1200px' }
      if(this.tutorialVisible) { return '1000px' }
      if(this.aboutVisible) { return '600px' }
      return '98%'
    }
  },
  methods: {
    closeDialog() {
      if (this.tutorialVisible) {
        this.$project.tutorial = false
        return
      }
      this.$project.report = false
      this.$project.keyfigures = false
      this.$project.about = false
      this.$project.scenario.editingModel = null
      this.$project.designState = {}
      this.$project.scenario.unsolved = true
    },
  }
}
</script>

<style>
#error {
  position: absolute;
  top: 0px;
  left: 0px;
  right: 0px;
  background: rgba(255, 0, 0, 0.9);
  color: #FFF;
  padding: 10px;
  text-align: center;
  font-size: 15px;
  font-weight: bold;
  z-index: 2;
}
body {
  padding: 0;
  margin: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.container {
  position: absolute;
  top: 0px;
  left: 0px;
  right: 0px;
}
.sub-container {
  height: calc(100vh - 71px);
}
.header {
  /* background: #FFF; */
  border-bottom: 1px solid #333;
  padding: 0px !important;
  height: auto !important;
}

.main {
  position: relative;
}
.sidebar {
  border-right: 1px solid #333;
  min-width: 340px;
  transition: all 0.5s;
  overflow-x: hidden;
  overflow-y: scroll;
}
.sidebar.hidden {
  width: 0px;
  min-width: 0px;
}
.sidebar-right {
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  transition: width 0.5s;
  overflow-x: hidden !important;
  overflow-y: scroll;
}
.sidebar-right.hidden {
  width: 0px;
}
#dialog {
  height: 1000px;
}
.el-dialog.default {
  margin-top: 15px !important;
  padding: 0px !important;
}
.el-dialog.init {
  margin-top: 250px !important;
  padding: 30px 30px !important;
  /* border: 3px solid #333; */
  border-radius: 15px;
}
.el-dialog.init .el-dialog__header {
  display: none !important;
}
.el-dialog.init .init-content {
  font-size: 1em;
  color: #333;
  width: 450px;
  text-align: center;
}
.init-title {
  font-size: 2.5em;
  font-weight: bold;
  color: #666;
  margin-bottom: 20px;
}
.el-dialog__header {
  padding: 10px !important;
}
/* HTML: <div class="loader"></div> */
.loader {
  margin: 0 auto;
  margin-bottom: 20px;
  width: 40px;
  aspect-ratio: 1;
  border-radius: 50%;
  border: 8px solid var(--el-color-primary);
  animation:
    l20-1 1.0s infinite linear alternate,
    l20-2 2.0s infinite linear;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}
.loader.loading {
  opacity: 1;
}
@keyframes l20-1{
   0%    {clip-path: polygon(50% 50%,0       0,  50%   0%,  50%    0%, 50%    0%, 50%    0%, 50%    0% )}
   12.5% {clip-path: polygon(50% 50%,0       0,  50%   0%,  100%   0%, 100%   0%, 100%   0%, 100%   0% )}
   25%   {clip-path: polygon(50% 50%,0       0,  50%   0%,  100%   0%, 100% 100%, 100% 100%, 100% 100% )}
   50%   {clip-path: polygon(50% 50%,0       0,  50%   0%,  100%   0%, 100% 100%, 50%  100%, 0%   100% )}
   62.5% {clip-path: polygon(50% 50%,100%    0, 100%   0%,  100%   0%, 100% 100%, 50%  100%, 0%   100% )}
   75%   {clip-path: polygon(50% 50%,100% 100%, 100% 100%,  100% 100%, 100% 100%, 50%  100%, 0%   100% )}
   100%  {clip-path: polygon(50% 50%,50%  100%,  50% 100%,   50% 100%,  50% 100%, 50%  100%, 0%   100% )}
}
@keyframes l20-2{ 
  0%    {transform:scaleY(1)  rotate(0deg)}
  49.99%{transform:scaleY(1)  rotate(135deg)}
  50%   {transform:scaleY(-1) rotate(0deg)}
  100%  {transform:scaleY(-1) rotate(-135deg)}
}

</style>
