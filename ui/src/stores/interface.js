import { defineStore } from 'pinia'

export const interfaceStore = defineStore('interface', {
  state: () => ({
    loading: false,
    report: false,
    tutorial: true,
    about: false,
    keyfigures: false,
    invalid: false,
    invalid_message: '',
    invalid_data: {},
    mouseMode: 'select',
    canvas: {
      grid: true,
      left: -5000,
      top: -5000,
      zoom: 1,
      zoomX: 0,
      zoomY: 0,
    },
    display: {
      debug: false,
      boosters: true,
      booster_info: true,
      flows: true,
      losses: true,
    },
    sidebar: {
      left: true,
      right: true,
    },
    lastAddedScenarioIndex: null,
    lastScenarioFeedback: null,
  }),
})
