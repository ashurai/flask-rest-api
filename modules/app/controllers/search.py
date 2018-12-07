''' Controller and routes to the search '''

import os
from flask import jsonify, request
import logger
from app import app, mongo
from app.schemas import validate_search
import sys
from urllib.parse import unquote
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/search', methods=['POST'])
def post_search():
    ''' Insert record related user search '''
    #return jsonify(request.get_json())
    data = validate_search(request.get_json())
    #print(data)
    if data['ok']:
        data = data['data']
        # Check user exist or not, if not then insert new user 
        user = common.check_user(data)
        # Insert new search history to the database
        searchObj = mongo.db.search.insert_one(data)
        # Update user search history 
        mongo.db.user.update({'_id': ObjectId(user)}, { '$push': {'searches': searchObj.inserted_id}})
        return jsonify({'ok': True, 'message': 'Search added to history successfuly!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters {}'. format(data['message'])}), 400

@app.route('/search/<emailId>', methods=['get'])
def get_search(emailId):
    ''' Get records from user searches '''
    if request.method == 'GET':
        query = request.args
        emailId = unquote(emailId)
        data = dumps(mongo.db.search.find({"emailId": emailId}))
        #print(data)
        return data, 200
        #return jsonify({'ok': True}, data), 200
        #return data, 200
