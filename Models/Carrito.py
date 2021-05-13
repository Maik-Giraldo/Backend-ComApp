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
        print(dataObject)
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

            resultados1 = self.ContadorCarrito (id_mesa)
            resultados2 =self.ContadorPlatillo (id_platillo, id_mesa)

            if resultados1 and resultados2:
                
    
                resultados_count = resultados1
                resultados_countPlatillo = resultados2 

                return jsonify({"transaccion": True, "resultados_count": resultados_count, "resultados_countPlatillo": resultados_countPlatillo})
            
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

            resultados = self.ContadorCarrito (id_mesa)
            if resultados:

                resultados_count = resultados
                return jsonify({"transaccion": True, "resultados_count": resultados_count})

            return jsonify({"transaccion": True})
            
        return jsonify({"transaccion": False})


    def ContadorCarrito(self, id_mesa):
        if id_mesa:
            resultados = mongo.db.carritoCompras.find({
                "id_mesa": id_mesa
            })

            if resultados:

                resultados_count = resultados.count()
                return resultados_count

            return 0

        return 0

    def ContadorPlatillo(self, id_platillo, id_mesa):
        if id_platillo and id_mesa:
            resultados = mongo.db.carritoCompras.find({
                "id_platillo": id_platillo,
                "id_mesa": id_mesa
            })
            if resultados:

                resultados_count = resultados.count()
                return resultados_count

            return 0
        return 0





    def ConfirmarPedido(self):       
        print("confimaste el pedido")
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        print(dataObject)
        

        search= mongo.db.carritoCompras.find(dataObject)

        i = search.count()

        for dat in mongo.db.carritoCompras.find(dataObject):
            print(dat)
            mongo.db.facturas.insert_one(dat)
        print("agredo correctamente")


        for dat in mongo.db.carritoCompras.find(dataObject):
            print(dat)
            mongo.db.carritoCompras.delete_one(dat)
        print("limpiar")



        return jsonify({"transaccion": True, "mensaje": "confirmar el pedido de forma exitosa"}),200



        
        
        
        
    def RechazarPedido(self):

        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_mesa = dataObject["id_mesa"]

        print("entro a rechazar el pedido")
        
        search= mongo.db.carritoCompras.find(dataObject)

        i = search.count()

        for dat in mongo.db.carritoCompras.find(dataObject):
            print(dat)
            mongo.db.carritoCompras.delete_one(dat)


        

                                                

        
        return jsonify({"transaccion": True, "mensaje": "rechazar el pedido de forma exitosa"}),200

        
    
        