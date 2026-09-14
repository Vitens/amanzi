# Amanzi
Amanzi is a design and scenario tool for drinking water treatment plants, developed by Vitens. We also have a hosted version of Amanzi available at https://demo.amanzi.app.

## Background
Developing scenarios for drinking water treatment plants is a complex task, as it involves many different factors and variables. Amanzi aims to simplify this process by providing a user-friendly interface for building and running scenarios. Amanzi allows for solving a treatment plant designs for quantity, quality, energy, chemicals and sustainability.

Amanzi works by generating a model file containing the separate scenarios. The model file is then parsed by the Python module and calculated for the different metrics.

## Installation
Amanzi can be run fully browser-based using Pyodide, or using a Python (flask) backend server. To use the browser-based version, simply download the latest release from the [releases page](https://github.com/Vitens/amanzi/releases) and start a local server to host the files, for example using Python's built-in HTTP server:
```bash
python -m http.server 8000
```
Then open the browser and navigate to http://localhost:8000.

## Development
When developing Amanzi, it is recommended to use the Python backend server as this allows for hot-reloading, faster development and easier debugging. In addition, the user interface must be started in development mode.

To start the Python backend server in development mode, create a virtual environment, install Amanzi and run the backend server:
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
amanzi-server --no-browser
```

To start the user interface in development mode, run the following command in the `ui` directory:
```bash
npm install
npm run dev
```
The user interface will now be available at http://localhost:5173

## License
Amanzi is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Documentation
User documentation lives in `docs/` and is built with [Zensical](https://zensical.org/). It follows [Diátaxis](https://diataxis.fr/map/) (tutorials, how-to guides, reference, explanation). From a virtual environment:

```bash
pip install -e ".[docs]"
zensical serve
```

Then open http://localhost:8000. Contributor and deployment notes stay in this README and in `lambda/README.md`; they are not part of the user site.

## Authors
- Abel Heinsbroek (Vitens N.V.)
- Nils Zickermann (Vitens N.V.)
- Christiaan Slippens (Vitens N.V.)
