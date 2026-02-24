import { loadPyodide, version as pyodideVersion} from 'pyodide'

export default {
  async initialize() {
    console.log(`Loading pyodide v${pyodideVersion}`)
    self.py = await loadPyodide(
      { indexURL: `https://cdn.jsdelivr.net/pyodide/v${pyodideVersion}/full/` }
    )

    await self.py.loadPackage('micropip')
    const pip = self.py.pyimport('micropip') 
    console.log('Installing phreeqpython')
    await pip.install('https://www.abelheinsbroek.nl/phreeqpython-1.6.0-py3-none-any.whl')
    console.log('Installing amanzi')
    await pip.install('https://www.abelheinsbroek.nl/amanzi-1.0.9-py2.py3-none-any.whl')


    const api = self.py.pyimport('amanzi.server.api')
    self.api = api.AmanziAPI()

  },

  async parameters() {
    return JSON.parse(self.api.parameters())
  },
  async keyfigures() {
    return JSON.parse(self.api.keyfigures())
  },
  async report(data) {
    return JSON.parse(self.api.report(JSON.stringify(data)))
  },
  async design(data, scenario, model) {
    return JSON.parse(self.api.design(JSON.stringify(data), scenario, model))
  },
  async solve(data, scenario) {
    return JSON.parse(self.api.solve(JSON.stringify(data), scenario))
  }



}