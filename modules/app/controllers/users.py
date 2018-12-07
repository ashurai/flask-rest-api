''' Controller to handle users required actions '''

import os
from flask import jsonify, request
import logger
from urllib.parse import unquote
from app import app, mongo
from bson.json_util import dumps

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/user/<emailId>', methods=['GET'])
def get_user(emailId):
    ''' Get Users bookmark by email id '''
    if request.method == 'GET':
        emailId = unquote(emailId)
        #return emailId
        data = dumps(mongo.db.user.find({'emailId': emailId}))
        return data, 200
