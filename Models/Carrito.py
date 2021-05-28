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
from datetime import datetime
from bson.objectid import ObjectId 
from bson import json_util, ObjectId
#Importacion de modelos



app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

#Clase agregar
class Carrito():
    def _init_(self):
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
        
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_mesa = dataObject["id_mesa"]
        date = datetime.now()
        id_pedido = None

        # Almacenar datos en la coleccion pedidos
        if id_mesa and date:

            maximo = mongo.db.pedido.find().sort("id_pedido", -1)
            cantidad = maximo.count()

            if cantidad > 0:

                data3 = list(maximo)
                data4 = json.loads(json_util.dumps(data3))
                dataObject1 = json.dumps(data4)
                dataObject2 = json.loads(dataObject1)
                id_pedido = int(dataObject2[0]["id_pedido"]) + 1
    
            else:
                id_pedido = 1

            myquery= {

                    "fechaHora": date,
                    "id_pedido": id_pedido,
                    "id_mesa": id_mesa

            }

            guardar = mongo.db.pedido.insert_one(myquery)

        # Almacenar datos en la coleccion detalle_pedido

        cantiCarrito = mongo.db.carritoCompras.find(dataObject)
        carritoData = list(cantiCarrito)
        carritoData1 = json.loads(json_util.dumps(carritoData))
        carritoDataObject = json.dumps(carritoData1)
        carritoDataObject1 = json.loads(carritoDataObject)
        cont1 = 0
        for dat in mongo.db.carritoCompras.find(dataObject):
            
            id_platillo = carritoDataObject1[cont1]["id_platillo"]
            precio_unitario = float(carritoDataObject1[cont1]["precio_unitario"])

            cantidad = mongo.db.carritoCompras.find({
                "id_platillo":id_platillo,
                "id_mesa": id_mesa
            }).count()
            

            validacion = mongo.db.detalle_pedido.find({
                "id_platillo":id_platillo,
                "id_pedido": id_pedido
            }).count()


            if validacion == 0:

                precio_total_platillo = precio_unitario * cantidad
                "COMENTARIO GUIA"
                myquery1 = {
                    "id_pedido" : id_pedido,
                    "id_platillo" : id_platillo,
                    "platillo_cantidad" : cantidad,
                    "precio_total_platillo": precio_total_platillo,
                    "estado": "P"

                }

                insertar = mongo.db.detalle_pedido.insert_one(myquery1)

            cont1 +=1

        for dat in mongo.db.carritoCompras.find(dataObject):

            mongo.db.carritoCompras.delete_one(dat)
  



        return jsonify({"transaccion": True, "mensaje": "confirmar el pedido de forma exitosa"}),200
  
        
    def RechazarPedido(self):

        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_mesa = dataObject["id_mesa"]

        search= mongo.db.carritoCompras.find(dataObject)

        i = search.count()

        for dat in mongo.db.carritoCompras.find(dataObject):
            print(dat)
            mongo.db.carritoCompras.delete_one(dat)

        return jsonify({"transaccion": True, "mensaje": "rechazar el pedido de forma exitosa"}),200

    def IngresarCliente(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)

        if dataObject:
            guardar = mongo.db.cliente.insert_one(dataObject)
        
        validacion = mongo.db.cliente.find_one(dataObject)

        if validacion:
            return jsonify({"transaccion": True, "mensaje": "Cliente exitoso"})
        
        return jsonify({"transaccion": False, "mensaje": "Ciente error"})


        
    
        