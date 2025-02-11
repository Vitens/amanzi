import _ from 'lodash'
import debounce from 'lodash/debounce';
import { defineStore } from 'pinia'
import { scenarioStore } from './scenario'


import axios from 'axios'

let url = import.meta.env.VITE_SERVER_URL

export const projectStore = defineStore('project', {
  state: () => ({
    name: 'Demo', // project name
    version: '0.0.1',    // project version
    debug: {},
    loading: true,
    report: false,
    tutorial: true,
    keyfigures: false,
    invalid: false,
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
    state: {}, // state of connections 
    designState: {}, // state of design
    reportState: {} // state of report
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
      // check if any scenario is unsaved
      for(var scenario of state.scenarios) {
        if(scenario.unsaved) {
          return true
        }
      }
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
    addScenario(name, duplicate) {
      // create new scenariostore
      var store = scenarioStore(Math.random().toString(36).substring(2, 8))
      // copy models and connections from current scenario
      if(duplicate) {
        store.models = _.cloneDeep(this.scenario.models)
        store.connections = _.cloneDeep(this.scenario.connections)
      }
      // set name
      store.name = name
      // set unsaved
      store.unsaved = true
      this.scenarios.push(store)
      // select new scenario
      this.selectedScenario = this.scenarios.length - 1
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

      var exportObject = {
        metadata: {
          version: this.version,
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
      let parameters = await axios.get(url + "/parameters")
      this.modelParameters = parameters.data
    },
    async getKeyFigures() {
      let parameters = await axios.get(url + "/keyfigures")
      console.log(parameters.data)
      return parameters.data.rows
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
          let response = await axios.post(url + "/report", this.serialize())
          this.reportState = response.data
        }
        else if (this.scenario.editingModel) {
          let response = await axios.post(url + "/design/" + this.selectedScenario + "/" + this.scenario.editingModel, this.serialize())
          this.designState = response.data
        } else {
          let response = await axios.post(url + "/solve/" + this.selectedScenario, this.serialize())
          this.state = response.data
        }
        this.invalid = false
      }
      catch (error) {
        this.invalid = true
      }
      this.loading = false
    }, 100, {leading: false, trailing: true}),    

    // load from http
    async open(defaultProject) {
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
      // unserialize project metadata
      this.name = project.metadata.project_name
      this.version = project.metadata.version
      this.keyfigureOverwrites = project.key_figure_overwrites
      if(project.metadata.canvas) {
        this.canvas = project.metadata.canvas
      }
      this.canvas.zoom = 1

      // dispose current scenarios
      for(var scenario of this.scenarios) {
        scenario.$dispose()
      }
      this.scenarios = []

      this.selectedScenario = 0

      // unserialize scenarios
      for(var scenario of project.scenarios) {
        // generate store with random uid
        var store = scenarioStore(Math.random().toString(36).substring(2, 8))
        store.name = scenario.name
        store.models = scenario.models
        store.connections = scenario.connections
        store.metaData = scenario.metaData
        store.keyfigureOverwrites = scenario.key_figure_overwrites

        this.scenarios.push(store)
      }

      this.scenario.unsolved = true
    }

  },

  persist: {
    enabled: false
  }
})
