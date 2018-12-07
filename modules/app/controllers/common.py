''' Controller to handle common components '''

from app import app, mongo
import logger
from bson.objectid import ObjectId
import json
from bson.json_util import dumps
import datetime

class common():
    def check_user(userData):
        user = userData['emailId']
        userObj = mongo.db.user.find_one({'emailId': user})
        #return dumps(userObj['_id'])
        if userObj is not None :
            return str(userObj.get('_id'))
        else :
            userObj = {'emailId': user, 'isDeleted': False, 'bookmarks': [], 'searches': [], 'dateCreated': datetime.datetime.now()}
            objectI = mongo.db.user.insert_one(userObj)
        return str(objectI.inserted_id)

