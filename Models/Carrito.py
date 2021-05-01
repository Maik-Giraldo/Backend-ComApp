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

#Clase agregar
class Carrito():
    def __init__(self):
        pass
    def Agregar(self):

        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['menu']['id_platillo']
        platillo = dataObject['menu']['platillo']
        descripcion = dataObject['menu']['descripcion']
        precio_unitario = dataObject['menu']['precio_unitario' ]
        tipo = dataObject['menu']['tipo']
        id_mesa = dataObject['id_mesa']

        myquery= {
            "id_platillo": id_platillo,
            "platillo": platillo,
            "descripcion": descripcion,
            "precio_unitario": precio_unitario,
            "tipo": tipo,
            "id_mesa": id_mesa 

        }

        if data:

            guardar = mongo.db.carritoCompras.insert_one(myquery)

            resultados = self.Contador (id_platillo)
            if resultados:

                resultados_count = resultados

                return jsonify({"transaccion": True, "resultados_count": resultados_count})
            
            return jsonify({"transaccion": True})
            
        return jsonify({"transaccion": False})

    def Eliminar(self):

            
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['menu']['id_platillo']
        id_mesa = dataObject["id_mesa"]

        if data and id_platillo:
            mongo.db.carritoCompras.delete_one({'id_platillo': id_platillo, "id_mesa": id_mesa})

            resultados = self.Contador(id_platillo)
            if resultados:

                resultados_count = resultados
                return jsonify({"transaccion": True, "resultados_count": resultados_count})

            return jsonify({"transaccion": True})
            
        return jsonify({"transaccion": False, "mensaje": "EL Platillo no existe"})

    def Contador(self, id_platillo):

        resultados = mongo.db.carritoCompras.find({
            "id_platillo": id_platillo
        })

        if resultados:

            resultados_count = resultados.count()

            return resultados_count
    
    def ResultadosCount(self):

        data = request.get_json()
        data2 = json.dumps(data)

        if data and data2:
            dataObject  = json.loads(data2)
            id_mesa = 1
            
            id_platillo = dataObject['id_platillo']

            resultados = mongo.db.carritoCompras.find({
                "id_platillo": id_platillo,
                "id_mesa": id_mesa
            })

            if resultados:

                resultados_count = resultados.count()

                if resultados_count:
                    return jsonify({"transaccion": True, "resultados_count": resultados_count})

                return jsonify({"transaccion": True, "resultados_count": 0})

            return jsonify({"transaccion": False, "resultados_count": 0})
        return jsonify({"transaccion": False, "resultados_count": 0})





