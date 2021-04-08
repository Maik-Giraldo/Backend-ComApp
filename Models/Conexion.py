#importacion de librerias necsarias
from flask_pymongo import PyMongo
from app import app


#conexion a la base de datos
app.config["MONGO_URI"]='mongodb://localhost/comApp'

mongo = PyMongo(app) 
