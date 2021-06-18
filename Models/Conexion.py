#importacion de librerias necesarias
from flask_pymongo import PyMongo
import json, datetime
from bson.objectid import ObjectId
from app import app

"""
@Class JSONEncoder
@param json.JSONEncoder
Desciprcion: clase utilizada para devolver archis JSON
@return 
"""
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,ObjectId):
            return str(o)

        if isinstance(o,datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self,o)

#conexion a la base de datos
app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority' 

mongo = PyMongo(app) 
app.json_encoder= JSONEncoder
