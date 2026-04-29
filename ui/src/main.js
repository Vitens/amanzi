import { createApp, ref } from 'vue'
import App from './App.vue'
import mitt from 'mitt'
import _ from 'lodash'
import { scenarioStore } from './stores/scenario'
import { projectStore } from './stores/project'
import { interfaceStore } from './stores/interface'
import { piniaUndoRedo } from './stores/undo'
import { createPinia } from 'pinia'
import VueCookies from 'vue-cookies'

import posthog from './plugins/posthog'
import api from './plugins/api'

import en from "./locales/en.json"
import nl from "./locales/nl.json"
import de from "./locales/de.json"

import {createI18n} from 'vue-i18n'

import ElementPlus from 'element-plus'
import * as Icons from '@element-plus/icons-vue' // Introduce all Icons and name them Icons

import NumberInput from './components/NumberInput.vue'

// import MasonryWall from '@yeger/vue-masonry-wall'
import VueMasonry from 'vue-masonry-css'

import pyodideBackend from './backend/python'
import serverBackend from './backend/server'

import 'font-awesome/css/font-awesome.css'
import 'element-plus/dist/index.css'

let version = __VERSION__

var chemform = function(chemical) {
  if(chemical == "") { return "" }

  let parts = chemical.match(/(\d+|[A-Za-z]+|\+|-)/g);

  let result = '';
  for (let part of parts) {
      if (/[A-Za-z]+/.test(part)) {
          result += part
      } else if (/\d+/.test(part)) {
          for (let char of part) {
              result += "<sub>"+char+"</sub>";
          }
      } else if (/\+|-/.test(part)) {
          for (let char of part) {
              result += "<sup>"+char+"</sup>";
          }
      }
  }

  return result;
}


// setup Pinia store
const pinia = createPinia()

// global variable for pinia
const shared = ref(100)
pinia.use(({store}) => {
  store.undo = shared
})

pinia.use(piniaUndoRedo)

// setup event bus
const eventBus = mitt()

// setup lodash
window._ = _

// setup i18n

const i18n = createI18n({
  locale: navigator.language.split('-')[0] || 'en',
  fallbackLocale: 'en',
  messages: { en, nl, de },
  silentTranslationWarn: true,
  fallbackWarn: false,
  missingWarn: false,
  legacy: false,
  globalInjection: true
})

let app = createApp(App)

// setup backend
if (import.meta.env.VITE_BACKEND == 'server') {
  app.config.globalProperties.$backend = serverBackend
} else {
  app.config.globalProperties.$backend = pyodideBackend
}

app.use(VueCookies)

app.use(pinia)
app.use(ElementPlus)
app.use(i18n)
app.use(VueMasonry)

for (let i in Icons) {
  app.component(i, Icons[i])
}

app.component('number-input', NumberInput)

// load models specification
var modelspec = {}
var modelVueNames = []

async function loadModels() {
  const models = import.meta.glob('./models/*/*.vue', {'eager': true})
  for(const path in models) {
    let split = path.split('/')
    let model = split[2]
    let type = split[3].split('.')[0]
    // let mdl = await modelVues[path]()
    let mdl = models[path]
    let name = _.startCase(_.camelCase(type+"-"+model)).replace(" ","")
    app.component(name, mdl.default)
    modelVueNames.push(name)

    if (type == 'block') {
      const properties = models[path].properties
      modelspec[model] = properties
    }
  }

}
// use posthog if not in development mode
if (import.meta.env.MODE != 'development') {
  app.use(posthog)
}

// let store use modelspec
pinia.use(({store}) => {
  store.modelspec = modelspec
})

await loadModels()

let store = projectStore()
let ui = interfaceStore()
store.currentAmanziVersion = version
store.$bus = eventBus
app.config.globalProperties.$bus = eventBus
app.config.globalProperties.modelspec = modelspec
app.config.globalProperties.$project = store
app.config.globalProperties.$interface = ui
app.config.globalProperties.chemform = chemform

app.config.globalProperties.$store = store.activeScenario
app.config.globalProperties.$modelVues = modelVueNames

app.config.globalProperties.$version = version

app.config.globalProperties.$http = api
app.mount('#app')
