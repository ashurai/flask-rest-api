''' Controller and routes to the bookmark '''

import os
from flask import jsonify, request
import logger
from app import app, mongo
from app.schemas import validate_bookmark
import sys
from urllib.parse import unquote
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from app.controllers.common import common
import json
from bson.objectid import ObjectId
import datetime

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

''' Add bookmark 
    Using bookmark Id '''
@app.route('/bookmark', methods=['POST'])
def post_bookmark():
    ''' Insert record related user bookmark '''
    #return jsonify(request.get_json())
    data = validate_bookmark(request.get_json())
    #return request.get_json()
    if data['ok']:
        data = data['data']
        # Check user exist or not, if not then insert new user 
        user = common.check_user(data)
        # Insert new bookmark to the record
        bookmarkObj = mongo.db.bookmark.insert_one(data)
        # Update user bookmarks after entry of bookmark
        mongo.db.user.update({'_id': ObjectId(user)}, { '$push': {'bookmarks': bookmarkObj.inserted_id}})
        return jsonify({'ok': True, 'message': 'bookmark added to history successfuly!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters {}'. format(data['message'])}), 400

''' Get User all bookmark's  
    Using bookmark Id '''
@app.route('/bookmark/<emailId>', methods=['GET', 'DELETE'])
def user_bookmark(emailId):
    ''' Get records from user bookmarks '''
    if request.method == 'GET':
        emailId = unquote(emailId)
        data = dumps(mongo.db.bookmark.find({'emailId': emailId, 'isDeleted': False}))
        return data, 200

''' Get bookmark 
    Using bookmark Id '''
@app.route('/bookmark/<bookmarkId>', methods=['GET'])
def get_bookmark(bookmarkId):
    ''' Get bookmark By Bookmark ID '''
    if request.method == 'GET':
        document = mongo.db.bookmark.find({'_id': ObjectId(bookmarkId)})
        if document is not None:
            return dumps(document), 200
        else:
            return jsonify({'ok': False, 'message': 'Bookmark does not belongs to this system!!'})

''' soft Delete bookmark
    Using bookmark Id '''
# TODO need to remove different routes to handle all operations of bookmark in one action after solving swagger api doc issue
@app.route('/bookmark/<bookmarkId>', methods=['DELETE'])
def delete_bookmark(bookmarkId):
    ''' Delete bookmark by Bookmark ID '''
    if request.method == 'DELETE':
        document = mongo.db.bookmark.find_one({'_id': ObjectId(bookmarkId)})
        #return dumps(document.get('isDeleted'))
        if document is not None and document.get('isDeleted') is None: 
            mongo.db.bookmark.update({'_id': ObjectId(bookmarkId)}, {'$set':{'isDeleted': True, 'active': False, 'dateDeleted': datetime.datetime.now()}}, {'multi': True}, upsert=True)
            return dumps(document), 200
        if document is not None and document.get('isDeleted') is True:
            return jsonify({'ok': True, 'message': 'Bookmark has been deleted already!'})
        else:
            return jsonify({'ok': False, 'message': 'Unable to delete bookmark!!'})

''' Update bookmark's methos 
    Using bookmark Id '''
# TODO need to remove different routes to handle all operations of bookmark in one action after solving swagger api doc issue
@app.route('/bookmark/<bookmarkId>', methods=['PUT'])
def put_bookmark(bookmarkId):
    ''' Update bookmark by Bookmark ID '''
    if request.method == 'PUT':
        data = validate_bookmark(request.get_json())
        if data['ok']:
            document = mongo.db.bookmark.find_one({'_id': ObjectId(bookmarkId)})
            #return dumps(data['data'])
            if document is not None: 
                mongo.db.bookmark.update_one({'_id': ObjectId(bookmarkId)}, {'$set': data['data']}, upsert=True)
                return dumps(document), 200
            else:
                return jsonify({'ok': False, 'message': 'Bookmark does not exists'})

