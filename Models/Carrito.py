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
from bson.objectid import ObjectId 
from bson import json_util, ObjectId
from datetime import datetime, timedelta
import pytz

#Conexion con MongoDB
app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

#Variable Global para el cliente
documentoCliente = None

#Clase carrito 
class Carrito():

    '''
    Class Carrito
    @Methods (Agregar, eliinar, contadorCarrito, contadorPlatillo, confirmarPedido, rechazar pedido, ingresarCliente)
    @return
    Responsable: Michael Giraldo, Andres taborda, Juan Leiton
    Descripcion: La clase carrito describe todos los metodos que se puedan realizar en el apartado del carrito u otras vistas desde donde se pueda interacturar con el carrito
    '''
    
    def _init_(self):
        pass


    """
    @Method Agregar
    @param self
    Desciprcion: metodo para agregar productos al carrito
    @return 
    """
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

        #Creacion de consulta
        myquery= {
            "id_platillo": id_platillo,
            "platillo": platillo,
            "descripcion": descripcion,
            "precio_unitario": precio_unitario,
            "tipo": tipo,
            "id_mesa": id_mesa 
        }

        #Aplicacion de la consulta
        if data and id_mesa:
            guardar = mongo.db.carritoCompras.insert_one(myquery)

            resultados1 = self.ContadorCarrito (id_mesa)
            resultados2 =self.ContadorPlatillo (id_platillo, id_mesa)

            if resultados1 and resultados2:
                resultados_count = resultados1
                resultados_countPlatillo = resultados2 
                return jsonify({"transaccion": True, "resultados_count": resultados_count, "resultados_countPlatillo": resultados_countPlatillo})
            return jsonify({"transaccion": True})
        return jsonify({"transaccion": False})

    """
    @Method Eliminar
    @param self
    Desciprcion: metodo para eliminar productos del carrito
    @return 
    """

    def Eliminar(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['menu']['id_platillo']
        id_mesa = dataObject["id_mesa"]

        #Consulta a base de datos
        if data and id_platillo:
            mongo.db.carritoCompras.delete_one({'id_platillo': id_platillo, "id_mesa": id_mesa})

            resultados = self.ContadorCarrito (id_mesa)

            if resultados == 0 or resultados != 0:

                resultados_count = resultados
                print(resultados_count)
                return jsonify({"transaccion": True, "resultados_count": resultados_count})
            return jsonify({"transaccion": True})
        return jsonify({"transaccion": False})

    
    """
    @Method ContadorCarrito
    @param self, id_mesa
    Desciprcion: metodo para contar los productos agregados al carrito
    @return 
    """

    def ContadorCarrito(self, id_mesa):
        #Consulta a base de datos
        if id_mesa:
            resultados = mongo.db.carritoCompras.find({
                "id_mesa": id_mesa
            })
            if resultados:
                resultados_count = resultados.count()
                return resultados_count
            return 0
        return 0


    """
    @Method ContadorPlatillo
    @param self, id_platillo, id_mesa
    Desciprcion: metodo para contar los productos agregados al carrito de una mesa en especifico
    @return 
    """
    def ContadorPlatillo(self, id_platillo, id_mesa):
        #consulta a base de datos
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

    """
    @Method ConfirmarPedido
    @param self
    Desciprcion: metodo para confirmar el pedido en conjunto
    @return 
    """

    def ConfirmarPedido(self):     
        documento_cliente = documentoCliente
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_mesa = dataObject["id_mesa"]
        utcmoment_naive = datetime.utcnow()
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
        co = 'America/Panama'
        date = utcmoment.astimezone(pytz.timezone(co)) - timedelta(hours = 5)
        print(date) 

        id_pedido = None
        
        # Almacenar datos en la coleccion pedidos
        if id_mesa and documento_cliente:
 
            maximo = mongo.db.pedido.find().sort("id_pedido", -1)
            cantidad = maximo.count()
  

            #Validacion
            if cantidad > 0:

 
                data3 = list(maximo)
                data4 = json.loads(json_util.dumps(data3))
                dataObject1 = json.dumps(data4)
                dataObject2 = json.loads(dataObject1)
                id_pedido = int(dataObject2[0]["id_pedido"]) + 1
    
            else:
                id_pedido = 1
            #Creacion de consulta para base de datos para agregar

            if id_pedido > 0:

                myquery= {
                        "fechaHora": date,
                        "id_pedido": id_pedido,
                        "id_mesa": id_mesa,
                        "estado": "pendiente"
                }
                #Aplicacion de consulta para agregar
                guardar = mongo.db.pedido.insert_one(myquery)

                #Creacion de consulta para base de datos para actualizar
                myquery2 = {'documento': str(documento_cliente)}
                newValues = {"$set": {
                    'id_pedido': id_pedido
                }}
                #Aplicacion de consulta para actualizar
                actualizar = mongo.db.cliente.update_one(myquery2, newValues)

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
                    "precio_total_platillo": precio_total_platillo

                }
                insertar = mongo.db.detalle_pedido.insert_one(myquery1)

            cont1 +=1

        for dat in mongo.db.carritoCompras.find(dataObject):
            mongo.db.carritoCompras.delete_one(dat)
        return jsonify({"transaccion": True, "mensaje": "confirmar el pedido de forma exitosa"}),200
  
    """
    @Method RechazarPedido
    @param self
    Desciprcion: metodo para rechazar el pedido en conjunto
    @return 
    """

    def RechazarPedido(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_mesa = dataObject["id_mesa"]

        #Consulta en base de datos para buscar en carrito compras
        search= mongo.db.carritoCompras.find(dataObject)

        i = search.count()

        for dat in mongo.db.carritoCompras.find(dataObject):
            #Consulta en base de datos para eliminar
            mongo.db.carritoCompras.delete_one(dat)
        return jsonify({"transaccion": True, "mensaje": "rechazar el pedido de forma exitosa"}),200

    """
    @Method IngresarCliente
    @param self
    Desciprcion: metodo para registrar los datos del cliente
    @return 
    """
    def IngresarCliente(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        global documentoCliente  
        documentoCliente = dataObject['documento']

        if dataObject:
            #Consulta base de datos para insertar un cliente
            guardar = mongo.db.cliente.insert_one(dataObject)
        validacion = mongo.db.cliente.find_one(dataObject)

        if validacion:
            return jsonify({"transaccion": True, "mensaje": "Cliente exitoso"})
        return jsonify({"transaccion": False, "mensaje": "Ciente error"})




        
    
        