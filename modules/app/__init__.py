''' User Search & Bookmark app '''

import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

class JSONEncoder(json.JSONEncoder):
    ''' extended to json encoder class '''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, ObjectId):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# Create the App Obj
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('DB')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.json_encoder = JSONEncoder

from app.controllers import *