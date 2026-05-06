# Amanzi

## Notes
Now supporting both Python (server) and Pyodide (client) backends.
To change the backend, set the VITE_BACKEND variable in your ui/.env file to 'pyodide' or 'server'.

### Pyodide backend
To use the Pyodide backend you need to place the python wheels in the ui/public/dist folder (create it if it doesn't exist).

The wheel for PhreeqPython can be downloaded from https://demo.amanzi.app/dist/phreeqpython-1.6.1-py3-none-any.whl

The wheel for Amanzi can be found at https://demo.amanzi.app/dist/amanzi-1.0.11-py2.py3-none-any.whl
Or can be built by running:

```bash
python -m build --wheel --outdir dist .
```

in the root directory of the project and copying the wheels to the ui/public/dist folder.
