// Create the worker instance (vite syntax)
const worker = new Worker(new URL('./python.worker.js', import.meta.url), { type: 'module' });

let msgId = 0;
const pendingRequests = new Map();

// Global listener for worker responses
worker.onmessage = (e) => {
  const { id, result, error } = e.data;
  const { resolve, reject } = pendingRequests.get(id);
  pendingRequests.delete(id);
  if (error) reject(new Error(error));
  else resolve(result);
};

// Helper to send messages to worker
function callWorker(method, args = {}) {
  const id = msgId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject });
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
  async initialize() {
    return callWorker('initialize');
  },
  async parameters() {
    return callWorker('parameters');
  },
  async keyfigures() {
    return callWorker('keyfigures');
  },
  async report(data) {
    return callWorker('report', { json: JSON.stringify(data) });
  },
  async design(data, scenario, model) {
    return callWorker('design', { data: JSON.stringify(data), scenario, model });
  },
  async solve(data, scenario) {
    return callWorker('solve', { data: JSON.stringify(data), scenario });
  }
};