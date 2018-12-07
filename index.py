""" Application boot or default call """
import os
import sys
from flask import jsonify, make_response
import connexion
from connexion.resolver import RestyResolver

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import logger
from app import app

# create a loger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# define the port variable to run the server 
PORT = os.environ.get('PORT')

@app.errorhandler(404)
def not_found(error):
    """ Error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'not found'}), 404)


@app.route("/")
def index():
    """ default home action """
    return jsonify({'data': 'Server running'}), 200

if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get("ENV"))
    # Create the application instance
    app = connexion.App(__name__, specification_dir='swagger/')
    # Read the swagger.yml file to configure the endpoints
    app.add_api('bookmarks-swagger.yaml', swagger_ui= True, resolver=RestyResolver('api'))
    app.run(host='0.0.0.0', port=4000, debug=True)
    #app.app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    #app.run(host='0.0.0.0', port=int(PORT))




