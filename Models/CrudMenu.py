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

"""
Clas menu
Responsable: Andres Taborda
Explain: Esta clase contiene distintos metodos que conforman todo el sistema del crud de un menu (crear, leer, actualizar, eliminar)
"""



class CrudMenu():
    def __init__(self):
        pass
    
    def mostrar(self):

        data = mongo.db.menu.find({})
        listado_documentos = list(data)
        id_mesa = 1

        if data == None:
            data = []

        return(listado_documentos)

    def mostrarcarrito(self):
        data = mongo.db.carritoCompras.find({'id_mesa' : 2})
        listado_carrito = list(data)

        if data == None:
            data = []

        return(listado_carrito)

        

    def crear(self):

        data = request.get_json()
        guardar = mongo.db.menu.insert_one(data)
        return jsonify({"transaccion": True, "mensaje": "Los datos se almacenaron de forma exitosa"})

    def actualizar(self):

        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['id_platillo']
        platillo = dataObject['platillo']
        descripcion = dataObject['descripcion']
        precio_unitario = dataObject['precio_unitario' ]
        tipo = dataObject['tipo']
        
        if data and id_platillo and platillo and descripcion and precio_unitario and tipo:

            myquery = {'id_platillo': id_platillo}
            newValues = {"$set": {
                'platillo': platillo,
                'descripcion' : descripcion,
                'precio_unitario' : precio_unitario,
                'tipo' : tipo 
            }}
            mongo.db.menu.update_one(myquery,newValues)

            return jsonify({"transaccion": True, "mensaje": "EL usuario fue actualizado satisfactoriamente"})
    def eliminar(self):

        
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
       
        id_platillo = dataObject['id_platillo']

        if data and id_platillo:
            mongo.db.menu.delete_one({'id_platillo': id_platillo})

            return jsonify({"transaccion": True, "mensaje": "EL usuario fue eliminado satisfactoriamente"})