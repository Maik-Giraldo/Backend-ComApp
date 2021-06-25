#Importacion de Librerias necesarias
from flask.views import MethodView
from flask import Flask, jsonify, request , session, render_template
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

#Importacion de libreria para correo
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import smtplib
from email.mime.text import MIMEText

#Conexion con base de datos
app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

'''
Class Personal Cocina
@Methods (Getfacturas, confirmarCocina, finalizarCocina, RechazarCocina, facturarCliente)
Desciprcion: clase en la que se desarrollan todos los metodos relacionados con el rol del personal de cocina
Responsable: Michael Giraldo, Andres taborda, Juan Leiton
'''
class PersonalCocina():
    
    def __init__(self):
        pass

    """
    @Method GetFacturas
    @param self
    Desciprcion: metodo para listar las facturas
    @return 
    """
    def GetFacturas(self):
        data = mongo.db.pedido_completo.find({})
        listado_pedido = list(data)
 
        if data == None:
            data = []

        return(listado_pedido)

    """
    @Method ConfirmarCocina
    @param self
    Desciprcion: metodo para confirmar un pedido pendiente
    @return 
    """
    def ConfirmarCocina(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        fechaHora = dataObject['fechaHora']
        id_pedido = dataObject['id_pedido']
        id_mesa = dataObject['id_mesa']
        detalle_pedido = dataObject['detalle_Pedido']
        precio_total = float(0)


        if id_pedido and id_mesa and fechaHora and detalle_pedido:
            for detalle in detalle_pedido:
                
                detalle2 = json.dumps(detalle)
                dataObject2 = json.loads(detalle2)
                precioTotalPlatillo = float(dataObject2['precio_total_platillo'])

                precio_total += precioTotalPlatillo

            myquery = {
                'id_pedido' : id_pedido,
                'id_mesa' : id_mesa,
                'fechaHora' : fechaHora,
                'precio_total': precio_total,
                'detalle_pedido' : detalle_pedido
            }
            precio_total = 0

            guardar = mongo.db.facturas.insert_one(myquery)

            myquery2 = {'id_pedido': int(id_pedido)}
            newValues = {"$set": {
                'estado': "confirmado"
            }}

            cambiarEstado = mongo.db.pedido.update_one(myquery2,newValues)

            #ENVIAR CORREO DE FACTURA
            factura = mongo.db.factura_final.find({'id_pedido': id_pedido})
            facturaData = list(factura)
            facturaData1 = json.loads(json_util.dumps(facturaData))

            cliente = facturaData1[0]['cliente']
            cliente2 = json.loads(json_util.dumps(cliente))
            correo = cliente2[0]['correo']




            subject = 'Factura de compra - ComApp'
            archivo = render_template("correoFactura.html",facturaData1 = facturaData1)

            proveedor_correo = 'smtp.live.com: 587'
            remitente = 'comapp.hw@hotmail.com'
            password = 'comapp123'
            #conexion a servidor
            servidor = smtplib.SMTP(proveedor_correo)
            servidor.starttls()
            servidor.ehlo()
            #autenticacion
            servidor.login(remitente, password)
            #mensaje 
            mensaje = archivo
            msg = MIMEMultipart()
            msg.attach(MIMEText(mensaje, 'html'))
            msg['From'] = remitente
            msg['To'] = str(correo)
            msg['Subject'] = ' COMAPP - Factura de compra'
            servidor.sendmail(msg['From'] , msg['To'], msg.as_string())

            return jsonify({"transaccion": True}),200
        
        return jsonify({"transaccion": False}),200

    """
    @Method FinalizarCocina
    @param self
    Desciprcion: metodo finalizar un pedido ya confirmado
    @return 
    """
    def FinalizarCocina(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_pedido = dataObject['id_pedido']



        if id_pedido:

            myquery = {'id_pedido': int(id_pedido)}
            newValues = {"$set": {
                'estado': "finalizado"
            }}

            cambiarEstado = mongo.db.pedido.update_one(myquery,newValues)

            return jsonify({"transaccion": True}),200
        return jsonify({"transaccion": False}),200

    """
    @Method RechazarCocina
    @param self
    Desciprcion: metodo para rechazar un pedido pendiente
    @return 
    """
    def RechazarCocina(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        fechaHora = dataObject['fechaHora']
        id_pedido = dataObject['id_pedido']
        id_mesa = dataObject['id_mesa']
        detalle_pedido = dataObject['detalle_Pedido']
        precio_total = float(0)

        if id_pedido:


            for detalle in detalle_pedido:
                
                detalle2 = json.dumps(detalle)
                dataObject2 = json.loads(detalle2)
                precioTotalPlatillo = float(dataObject2['precio_total_platillo'])

                precio_total += precioTotalPlatillo

            cliente = mongo.db.cliente.find({'id_pedido': id_pedido})

            if cliente:
                cliente2 = json.loads(json_util.dumps(cliente))
                correo = cliente2[0]['correo']

                myquery2 = {
                    'id_pedido' : id_pedido,
                    'id_mesa' : id_mesa,
                    'fechaHora' : fechaHora,
                    'precio_total': precio_total,
                    'detalle_pedido' : detalle_pedido,
                }

                #Consulta en base de datos para generar mensaje de rechazo de pedido por correo
                rechazo = mongo.db.pedidos_rechazados.insert_one(myquery2)
                pedidoRechazado = mongo.db.pedidos_rechazados.find({'id_pedido':id_pedido, 'fechaHora' : fechaHora})
                facturaData = list(pedidoRechazado)
                facturaData1 = json.loads(json_util.dumps(facturaData))

                #ENvio del correo
                subject = 'Ocurrio un error con tu pedido - ComApp'
                archivo = render_template("correoRechazo.html",facturaData1 = facturaData1, cliente = cliente2)

                proveedor_correo = 'smtp.live.com: 587'
                remitente = 'comapp.hw@hotmail.com'
                password = 'comapp123'
                #conexion a servidor
                servidor = smtplib.SMTP(proveedor_correo)
                servidor.starttls()
                servidor.ehlo()
                #autenticacion
                servidor.login(remitente, password)
                #mensaje 
                mensaje = archivo
                msg = MIMEMultipart()
                msg.attach(MIMEText(mensaje, 'html'))
                msg['From'] = remitente
                msg['To'] = str(correo)
                msg['Subject'] = ' COMAPP - Error con tu pedido, pedido cancelado'
                servidor.sendmail(msg['From'] , msg['To'], msg.as_string())


            myquery = {'id_pedido': int(id_pedido)}
            newValues = {"$set": {
                'estado': "rechazado"
            }}

            cambiarEstado = mongo.db.pedido.update_one(myquery,newValues)
            eliminarCliente = mongo.db.cliente.delete_one({'id_pedido': id_pedido})

            return jsonify({"transaccion": True}),200
        
        return jsonify({"transaccion": False}),200

    """
    @Method FacturaCliente
    @param self
    Desciprcion: metodo para listar las facturas de un cliente
    @return 
    """
    def FacturaCliente(self):
        #Buscar factura por cliente
        data = mongo.db.factura_final.find({})

        listado_pedido = list(data)
 
        if data == None:
            data = []

        return (listado_pedido)



