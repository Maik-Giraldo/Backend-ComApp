#importacion de librerias necsarias
from flask_pymongo import PyMongo
import json, datetime
from bson.objectid import ObjectId
from app import app

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,ObjectId):
            return str(o)

        if isinstance(o,datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self,o)

#conexion a la base de datos
app.config["MONGO_URI"]='mongodb://localhost/comApp'

mongo = PyMongo(app) 
app.json_encoder= JSONEncoder
