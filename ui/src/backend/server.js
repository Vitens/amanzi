// Axios backend wrapper for external Amanzi server API

import axios from 'axios'

let url = import.meta.env.VITE_SERVER_URL

export default {
  async parameters() {
    let parameters = await axios.get(url + '/parameters')
    return parameters.data
  },
  async keyfigures() {
    let keyfigures = await axios.get(url + '/keyfigures')
    return keyfigures.data
  },
  async report(data) {
    let report = await axios.post(url + '/report', data)
    return report.data
  },
  async design(data, scenario, model) {
    let design = await axios.post(url + '/design/' + scenario + '/' + model, data)
    return design.data
  },
  async solve(data, scenario) {
    let solve = await axios.post(url + '/solve/' + scenario, data)
    return solve.data
  }

}