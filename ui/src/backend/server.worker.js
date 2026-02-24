// Web Worker for HTTP requests to external Amanzi server API

import axios from 'axios'

const url = import.meta.env.VITE_SERVER_URL

self.onmessage = async (event) => {
  const { id, method, args } = event.data

  try {
    let result
    switch (method) {
      case 'initialize':
        result = true
        break
      case 'parameters': {
        const parameters = await axios.get(url + '/parameters')
        result = parameters.data
        break
      }
      case 'keyfigures': {
        const keyfigures = await axios.get(url + '/keyfigures')
        result = keyfigures.data
        break
      }
      case 'report': {
        const report = await axios.post(url + '/report', args.data)
        result = report.data
        break
      }
      case 'design': {
        const design = await axios.post(url + '/design/' + args.scenario + '/' + args.model, args.data)
        result = design.data
        break
      }
      case 'solve': {
        const solve = await axios.post(url + '/solve/' + args.scenario, args.data)
        result = solve.data
        break
      }
      default:
        throw new Error(`Unknown method: ${method}`)
    }
    self.postMessage({ id, result })
  } catch (error) {
    self.postMessage({ id, error: error?.message ?? String(error) })
  }
}
