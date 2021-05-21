#Importacion de Librerias necesarias
from flask.views import MethodView
from flask import Flask, jsonify, request , session
from flask_pymongo import PyMongo
import json
from flask import jsonify, request
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import bcrypt
from flask_bcrypt import Bcrypt 
import binascii
from app import app

#Importacion de modelos


app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


class PersonalCocina():
    def __init__(self):
        pass

    
    def GetFacturas(self):
        print("ssss")
        data = mongo.db.facturas.find({})
        listado_facturas = list(data)


        if data == None:
            data = []

        return(listado_facturas)
