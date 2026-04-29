import os
import click
import webbrowser

from .api import AmanziAPI

from flask import Flask, request, send_from_directory, abort
from flask_cors import CORS


# get module directory and go up two levels
module_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# check if ui/dist exists in the module directory, if not append amanzi to the path (whl install)
if not os.path.exists(os.path.join(module_dir, 'ui', 'dist')):
    # append amanzi to the path
    module_dir = os.path.join(module_dir, 'amanzi')

app = Flask(__name__, static_folder=os.path.join(module_dir, 'ui', 'dist'))
CORS(app)

# initialize api
api = AmanziAPI()

# Route to serve files from the dist folder
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/parameters', methods=['GET'])
def parameters():
    return api.parameters()

@app.route('/api/solve/<scenario>', methods=['POST'])
def solve(scenario):
    return api.solve(request.json, scenario)
    
@app.route('/api/report', methods=['POST'])
def report():
  return api.report(request.json)

@app.route('/api/design/<scenario>/<model>', methods=['POST'])
def design(scenario, model):
  return api.design(request.json, scenario, model)

@app.route('/api/keyfigures', methods=['GET'])
def keyfigures():
  return api.keyfigures()

@click.command()
@click.option('--debug', is_flag=True, help='Run in debug mode', default=False)
@click.option('--port', type=int, help='Port to run on', default=7331)
@click.option('--no-browser', is_flag=True, help='Do not open browser', default=False)
def main(debug, port, no_browser):

    banner = [   r"   _                                  _ ", r"  /_\   _ __ ___    __ _  _ __   ____(_)", r" //_\\ | '_ ` _ \  / _` || '_ \ |_  /| |", r"/  _  \| | | | | || (_| || | | | / / | |", r"\_/ \_/|_| |_| |_| \__,_||_| |_|/___||_|"]

    for line in banner:
        click.echo(line)

    # open browser

    if not no_browser:
        webbrowser.open(f'http://localhost:{port}')

    app.run(debug=debug, port=port)
