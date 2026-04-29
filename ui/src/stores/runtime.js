import { defineStore } from 'pinia'

export const runtimeStore = defineStore('runtime', {
  state: () => ({
    solveState: {},
    designState: {},
    reportState: {},
  }),
})
