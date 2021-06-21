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

#Importacion de librerias necesarias para imagenes en nube
import os
from PIL import Image
from io import BytesIO  
import base64
import dropbox
import random

#Conexion con base de datos
app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

"""
Clase CrudMenu
Responsable: Andres Taborda
Explain: Esta clase contiene distintos metodos que conforman todo el sistema del crud de un menu (crear, leer, actualizar, eliminar)
"""
class CrudMenu():
    def __init__(self):
        pass
    
    """
    @Method mostrar
    @param self
    Desciprcion: metodo para mostrar cada platillo del menu
    @return 
    """
    def mostrar(self):

        data = mongo.db.menu.find({})
        listado_documentos = list(data)

        if data == None:
            data = []

        return(listado_documentos)

    """
    @Method mostrarcarrito
    @param self
    Desciprcion: metodo para listar los elementos del carrito
    @return 
    """
    def mostrarcarrito(self):
        id_mesa = self.id_mesa
        data = mongo.db.carritoCompras.find({'id_mesa' : id_mesa})
        listado_carrito = list(data)

        if data == None:
            data = []

        return(listado_carrito)

    """
    @Method crear
    @param self
    Desciprcion: metodo para crear platillos
    @return 
    """
    def crear(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = int(dataObject['id_platillo'])
        platillo = dataObject['platillo']
        descripcion = dataObject['descripcion']
        precio_unitario = float(dataObject['precio_unitario' ])
        tipo = dataObject['tipo']
        img = dataObject['img']
        img_final = ''
        
        #validacion para guardar tipos de imagen (git, jpeg y png)
        if "data:image/gif;base64," in img:
            img_final = img[22::]

        elif "data:image/jpeg;base64," in img:
            img_final = img[23::]

        elif "data:image/png;base64," in img:
            img_final = img[22::]
        
        else:
            return jsonify({}), 200

        #Proceso para guardar imagen en la nube
        nameImg = str(platillo)
        im = Image.open(BytesIO(base64.b64decode(img_final)))
        im.save('{}'.format(nameImg+'.png'), 'PNG')
        nombre_image = nameImg+'.png'

        key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+%$'
        
        string_random = ''.join(random.sample(key, 64))

        nombre = string_random + platillo + '.jpg'

        result = ''

        dbx = dropbox.Dropbox('i55bkV3doxoAAAAAAAAAAZHHYiUBwkXoHtTHt-S-1R7WmzjiR3CF1qH3LydQ4WEA')

        with open(nombre_image, 'rb') as f:
            result = dbx.files_upload(f.read(), '/ComApp/Menu/' + nombre)

        os.remove(nombre_image)

        link = dbx.sharing_create_shared_link(path='/ComApp/Menu/' + nombre)

        link_image = link.url.replace('?dl=0', '?dl=1')

        #Creacion de consulta para agregar nuevo platillo al menu
        myquery = {
            "id_platillo" : int(id_platillo),
            "platillo": platillo,
            "descripcion": descripcion,
            "precio_unitario": float(precio_unitario),
            "tipo": tipo,
            "img": link_image
        }
        #Aplicacion de consulta
        guardar = mongo.db.menu.insert_one(myquery)
        return jsonify({"transaccion": True, "mensaje": "Los datos se almacenaron de forma exitosa"})

    """
    @Method actualizar
    @param self
    Desciprcion: metodo para actualizar un platillo
    @return 
    """
    def actualizar(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = int(dataObject['id_platillo'])
        platillo = dataObject['platillo']
        descripcion = dataObject['descripcion']
        precio_unitario = float(dataObject['precio_unitario' ])
        tipo = dataObject['tipo']
        img = dataObject['img']
        img_final = ''

        #Variable de validacion para saber si se inserta nueva imagen o se esta actualizando.
        imagen_cambio = False
        link_image = img

        if "data:image/gif;base64," in img:
            img_final = img[22::]
            imagen_cambio = True

        if "data:image/jpeg;base64," in img:
            img_final = img[23::]
            imagen_cambio = True

        if "data:image/png;base64," in img:
            img_final = img[22::]
            imagen_cambio = True
        
        #Validacion de si se inserta una nueva imagen o se actualiza
        if imagen_cambio: 
            nameImg = str(platillo)
            im = Image.open(BytesIO(base64.b64decode(img_final)))
            im.save('{}'.format(nameImg+'.png'), 'PNG')
            nombre_image = nameImg+'.png'

            key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+%$'
            
            string_random = ''.join(random.sample(key, 64))

            nombre = string_random + platillo + '.jpg'

            result = ''

            dbx = dropbox.Dropbox('i55bkV3doxoAAAAAAAAAAZHHYiUBwkXoHtTHt-S-1R7WmzjiR3CF1qH3LydQ4WEA')

            with open(nombre_image, 'rb') as f:
                result = dbx.files_upload(f.read(), '/ComApp/Menu/' + nombre)

            os.remove(nombre_image)

            link = dbx.sharing_create_shared_link(path='/ComApp/Menu/' + nombre)

            link_image = link.url.replace('?dl=0', '?dl=1')

        

        if data and id_platillo and platillo and descripcion and precio_unitario and tipo:

            myquery = {'id_platillo': int(id_platillo)}
            newValues = {"$set": {
                'platillo': platillo,
                'descripcion' : descripcion,
                'precio_unitario' : float(precio_unitario),
                'tipo' : tipo, 
                'img' : link_image
            }}
            mongo.db.menu.update_one(myquery,newValues)

            return jsonify({"transaccion": True, "mensaje": "El platillo fue actualizado satisfactoriamente"})
        # return jsonify({"transaccion": True, "mensaje":})
    
    """
    @Method eliminar
    @param self
    Desciprcion: metodo para eliminar un platillo en especifico
    @return 
    """
    def eliminar(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
       
        id_platillo = int(dataObject['id_platillo'])

        #Consulta para eliminar por Id de platillo
        if data and id_platillo:
            mongo.db.menu.delete_one({'id_platillo': id_platillo})

            return jsonify({"transaccion": True, "mensaje": "EL usuario fue eliminado satisfactoriamente"})