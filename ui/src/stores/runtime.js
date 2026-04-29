import { defineStore } from 'pinia'

export const runtimeStore = defineStore('runtime', {
  state: () => ({
    state: {},
    designState: {},
    reportState: {},
  }),
})
