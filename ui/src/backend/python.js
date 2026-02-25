// Create the worker instance (vite syntax)
const worker = new Worker(new URL('./python.worker.js', import.meta.url), { type: 'module' });

let msgId = 0;
const pendingRequests = new Map();

// Global listener for worker responses
worker.onmessage = (e) => {
  const { id, result, error, progress } = e.data;
  const { resolve, reject, onProgress } = pendingRequests.get(id);

  if (onProgress && progress !== undefined) { 
    onProgress(progress);
    return;
  }

  pendingRequests.delete(id);
  if (error) reject(new Error(error));
  else resolve(result);
};

// Helper to send messages to worker
function callWorker(method, args = {}, onProgress = null) {
  const id = msgId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject, onProgress });
    try {
      worker.postMessage({ id, method, args });
    }
    catch (error) {
      pendingRequests.delete(id);
      console.error(error);
      reject(new Error(error));
    }
  });
}

export default {
  driver: 'pyodide',
  async initialize(onProgress) {
    return callWorker('initialize', {}, onProgress);
  },
  async parameters() {
    return callWorker('parameters');
  },
  async keyfigures() {
    return callWorker('keyfigures');
  },
  async report(data) {
    return callWorker('report', { data: JSON.stringify(data) });
  },
  async design(data, scenario, model) {
    return callWorker('design', { data: JSON.stringify(data), scenario, model });
  },
  async solve(data, scenario) {
    return callWorker('solve', { data: JSON.stringify(data), scenario });
  }
};