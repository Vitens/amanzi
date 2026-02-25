import { loadPyodide, version as pyodideVersion } from 'pyodide';

let api;

// 1. Setup Pyodide inside the worker
async function initPyodide(id) {

  const sendProgress = (value, message) => {
    self.postMessage({ id, progress: { value, message } });
  }

  sendProgress(0, 'Loading Pyodide...');
  const py = await loadPyodide({
    indexURL: `https://cdn.jsdelivr.net/pyodide/v${pyodideVersion}/full/`
  });
  sendProgress(20, 'Loading Micropip...');
  await py.loadPackage('micropip');
  const pip = py.pyimport('micropip');
  
  sendProgress(40, 'Loading PhreeqPython...');
  await pip.install('/dist/phreeqpython-1.6.1-py3-none-any.whl');
  sendProgress(60, 'Loading Amanzi Solver...');
  await pip.install('/dist/amanzi-1.0.11-py2.py3-none-any.whl');

  sendProgress(80, 'Starting Amanzi API...');

  const apiModule = py.pyimport('amanzi.server.api');
  api = apiModule.AmanziAPI();

  sendProgress(100, 'Loading done!');

  return true;
}

// 2. Handle incoming messages
self.onmessage = async (event) => {
  const { id, method, args } = event.data;

  try {
    let result;
    switch (method) {
      case 'initialize':
        result = await initPyodide(id);
        break;
      case 'parameters':
        result = JSON.parse(api.parameters());
        break;
      case 'keyfigures':
        result = JSON.parse(api.keyfigures());
        break;
      case 'report':
        result = JSON.parse(api.report(args.data));
        break;
      case 'design':
        result = JSON.parse(api.design(args.data, args.scenario, args.model));
        break;
      case 'solve':
        result = JSON.parse(api.solve(args.data, args.scenario));
        break;
      default:
        throw new Error(`Unknown method: ${method}`);
    }
    self.postMessage({ id, result });
  } catch (error) {
    console.error(error)
    self.postMessage({ id, error: error.message });
  }
};