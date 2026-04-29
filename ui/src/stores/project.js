import _ from 'lodash'
import debounce from 'lodash/debounce';
import { defineStore } from 'pinia'
import { scenarioStore } from './scenario'
import { migrateProject } from '../lib/projectMigration'

export const projectStore = defineStore('project', {
  state: () => ({
    name: 'Demo', // project name
    version: '0.0.1',    // project version
    debug: {},
    loading: false,
    report: false,
    tutorial: true,
    about: false,
    keyfigures: false,
    invalid: false,
    backend: null,
    mouseMode: 'select',
    display: {
      debug: false,
      boosters: true,
      booster_info: true,
      flows: true,
      losses: true,
    },
    canvas: {
      grid: true,
      left: -5000,
      top: -5000,
      zoom: 1,
      zoomX: 0,
      zoomY: 0,
    },          // canvas state
    sidebar: {
      left: true,
      right: true
    },
    keyfigureOverwrites: {},
    modelParameters: {},
    scenarios: [
      scenarioStore(1),
    ],       // list of scenarios
    selectedScenario: 0, // index of selected scenario
    lastAddedScenarioIndex: null, // briefly set after add/duplicate for tab pulse
    lastScenarioFeedback: null, // { messageKey } for centered message (add or duplicate)
    state: {}, // state of connections 
    designState: {}, // state of design
    reportState: {}, // state of report
    lastMigrationChanges: [], // migration toast rows; cleared in notifyMigrationIfNeeded
    migrationAppliedOnLastOpen: false,
    migrationNotifyFrom: '',
    migrationNotifyTo: '',
    currentAmanziVersion: '',
  }),
  getters: {
    scenario: (state) => {
      return state.scenarios[state.selectedScenario]
    },
    number_of_overwrites: (state) => {
      let set = new Set(Object.keys(state.keyfigureOverwrites).concat(Object.keys(state.scenarios[state.selectedScenario].keyfigureOverwrites)))
      return set.size
    },
    unsaved: (state) => {
      for (var scenario of state.scenarios) {
        if (scenario.unsaved) return true
      }
      return false
    },
  },
  actions: {
    edit_key_figures() {
      this.keyfigures = true
    },
    run_report() { 
      this.report = true
      this.solveDebounced()
    },
    // patch undo
    patchUndo(state) {
      this.selectedScenario = state.selectedScenario
    },
    newProject() {
      this.name = 'New project'
      this.scenarios = []
      this.selectedScenario = 0
      this.addScenario('Scenario 1')
    },

    selectScenario(index) {
      this.$pushUndo({
        selectedScenario: this.selectedScenario
      })
      this.selectedScenario = index
      // clear state and set unsolved
      this.state = {}
      this.scenario.unsolved = true
    },

    // scenario management
    generateUID() {
      return Math.random().toString(36).substring(2, 8);
    },

    // remap connection cid "src -> tgt (type)" to use new UIDs
    remapCid(cid, uidMap) {
      const match = cid.match(/^(.+?) -> (.+?) \((.+)\)$/)
      if (!match) return cid
      const [, src, tgt, type] = match
      return (uidMap[src] || src) + ' -> ' + (uidMap[tgt] || tgt) + ' (' + type + ')'
    },

    remapStateForDuplicate(state, uidMap) {
      const connections = {}
      if (state.connections) {
        for (const cid of Object.keys(state.connections)) {
          connections[this.remapCid(cid, uidMap)] = state.connections[cid]
        }
      }
      const hydraulics = {}
      if (state.hydraulics) {
        for (const uid of Object.keys(state.hydraulics)) {
          const newUid = uidMap[uid]
          if (newUid) hydraulics[newUid] = state.hydraulics[uid]
        }
      }
      return _.assign({}, state, { connections, hydraulics })
    },

    remapDesignStateForDuplicate(designState, uidMap) {
      const hydraulics = {}
      if (designState.hydraulics) {
        hydraulics.connections = {}
        if (designState.hydraulics.connections) {
          for (const cid of Object.keys(designState.hydraulics.connections)) {
            hydraulics.connections[this.remapCid(cid, uidMap)] = designState.hydraulics.connections[cid]
          }
        }
        hydraulics.models = {}
        if (designState.hydraulics.models) {
          for (const uid of Object.keys(designState.hydraulics.models)) {
            const newUid = uidMap[uid]
            if (newUid) hydraulics.models[newUid] = designState.hydraulics.models[uid]
          }
        }
      }
      return _.assign({}, designState, { hydraulics })
    },

    addScenario(name, duplicate) {
      // create new scenariostore
      var store = scenarioStore(Math.random().toString(36).substring(2, 8))
      // copy models and connections from current scenario
      if(duplicate) {
        store.models = _.cloneDeep(this.scenario.models)
        store.connections = _.cloneDeep(this.scenario.connections)

        // build old UID -> new UID map and assign new UIDs to cloned models
        let uidMap = {}
        for (var model of store.models) {
          let newUid = this.generateUID()
          uidMap[model.uid] = newUid
          model.uid = newUid
        }
        // update cloned connections to use new UIDs (don't mutate this.scenario!)
        for (var connection of store.connections) {
          connection.src = uidMap[connection.src]
          connection.tgt = uidMap[connection.tgt]
        }
        store.metaData = _.cloneDeep(this.scenario.metaData)
        store.keyfigureOverwrites = _.cloneDeep(this.scenario.keyfigureOverwrites)

        // reuse original scenario's solve/design state with remapped UIDs
        if (this.state && this.state.connections) {
          this.state = this.remapStateForDuplicate(this.state, uidMap)
        }
        if (this.designState && this.designState.hydraulics) {
          this.designState = this.remapDesignStateForDuplicate(this.designState, uidMap)
        }
      }

      // set name
      store.name = name
      
      // set unsaved
      store.unsaved = true

      this.scenarios.push(store)
      // select new scenario
      this.selectedScenario = this.scenarios.length - 1
      // feedback: pulse the new tab (new or duplicate) and show centered message
      const newIndex = this.scenarios.length - 1
      this.lastAddedScenarioIndex = newIndex
      this.lastScenarioFeedback = { messageKey: duplicate ? 'ui.scenariobar.scenario_duplicated' : 'ui.scenariobar.scenario_created' }
      setTimeout(() => { this.lastAddedScenarioIndex = null }, 900)
      setTimeout(() => { this.lastScenarioFeedback = null }, 1800)
    },

    renameScenario(newName) {
      this.scenarios[this.selectedScenario].name = newName
    },
    removeScenario() {
      this.scenarios.splice(this.selectedScenario, 1)
      this.selectedScenario = 0
    },
    resetScenario() {
      this.scenarios[this.selectedScenario].$reset()
    },

    initialize() {
      // initialize from local storage, load JSON

    },
    save() {
      // save to local storage
      localStorage.setItem('project', JSON.stringify(this.serialize()))
      // mark all scenarios as saved
      for(var scenario of this.scenarios) {
        scenario.unsaved = false
      }
    },

    // serialize to json
    serialize() {

      const currentVersion = this.currentAmanziVersion || this.version || '0.0.0'
      var exportObject = {
        metadata: {
          version: this.version,
          amanzi_version: currentVersion,
          project_name: this.name,
          canvas: this.canvas
        },
        key_figure_overwrites: this.keyfigureOverwrites,
        scenarios: []
      }

      for(var scenario of this.scenarios) {
        exportObject.scenarios.push(scenario.serialize())
      }

      return exportObject
    },

    async solve() {
      this.solveDebounced()
    },

    async loadParameters(type) {
      this.modelParameters = await this.backend.parameters()
      for(var scenario of this.scenarios) {
        scenario.checkAndUpdateModelParameters(this.modelParameters)
      }
    },
    async getKeyFigures() {
      let keyfigures = await this.backend.keyfigures()
      return keyfigures.rows
    },

    solveDebounced: debounce(async function () {
      // solve network or single model
      this.loading = true



      let valid = this.scenario.validate()
      if(!valid.valid) {
        this.invalid = true
        this.invalid_message = valid.message
        this.invalid_data = valid.data
        this.loading = false
        return
      }

      try {
        if(this.report) {
          let response = await this.backend.report(this.serialize())
          this.reportState = response
        }
        else if (this.scenario.editingModel) {
          let response = await this.backend.design(this.serialize(), this.selectedScenario, this.scenario.editingModel)
          this.designState = response
        } else {
          let response = await this.backend.solve(this.serialize(), this.selectedScenario)
          this.state = response
        }
        this.invalid = false
      }
      catch (error) {
        this.invalid = true
      }
      this.loading = false
    }, 200, {leading: false, trailing: true}),    

    // load from http
    async open(defaultProject, updateParameters=true) {
      // fetch project file from url
      var project = {}
      if(localStorage.getItem('project')) {
        project = JSON.parse(localStorage.getItem('project'))
      } else {
        project = defaultProject
      }
      if(!project) {
        return
      }

      const currentVersion = this.currentAmanziVersion || '0.0.0'
      this.lastMigrationChanges = []
      this.migrationAppliedOnLastOpen = false
      this.migrationNotifyFrom = ''
      this.migrationNotifyTo = ''
      try {
        const result = migrateProject(project, currentVersion)
        project = result.project
        this.lastMigrationChanges = result.changes || []
        this.migrationAppliedOnLastOpen = !!result.migrated
        if (result.migrated) {
          this.migrationNotifyFrom = result.fromVersion || ''
          this.migrationNotifyTo = result.toVersion || ''
        }
      } catch (err) {
        console.warn('Project migration failed', err)
      }

      // unserialize project metadata
      this.name = project.metadata?.project_name ?? this.name
      this.version = project.metadata?.version ?? this.version
      this.keyfigureOverwrites = project.key_figure_overwrites || {}
      if(project.metadata?.canvas) {
        this.canvas = { ...this.canvas, ...project.metadata.canvas }
      }
      this.canvas.zoom = 1

      // dispose current scenarios
      for(var scenario of this.scenarios) {
        scenario.$dispose()
      }
      this.scenarios = []

      this.selectedScenario = 0

      // unserialize scenarios
      for(var scenario of project.scenarios || []) {
        var store = scenarioStore(Math.random().toString(36).substring(2, 8))
        store.name = scenario.name
        store.notes = scenario.notes ?? ''
        store.models = scenario.models || []
        store.connections = scenario.connections || []
        store.metaData = scenario.metaData
        store.keyfigureOverwrites = scenario.key_figure_overwrites || {}

        if(updateParameters) {
          store.checkAndUpdateModelParameters(this.modelParameters)
        }

        this.scenarios.push(store)
      }
      this.scenario.unsolved = true

      if (this.migrationAppliedOnLastOpen) {
        this.save()
      }

      if (this.migrationAppliedOnLastOpen) {
        this.$bus?.emit('migration-notify')
      }
    }

  }
})
