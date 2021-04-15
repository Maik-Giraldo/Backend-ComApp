from flask.views import MethodView
from flask import Flask, jsonify, request , session
import json
from flask import jsonify, request
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import bcrypt
import binascii
from app import app

#Importacion de modelos
from Models.Qrcode import Qrcode
from Models.Conexion import * 
from Models.PeticionAgregar import Peticion
from Models.Carrito import Carrito


'''
Clase CodigoQR
Responsable Michael Giraldo
Methods POST
'''
class QrCodeControllers(MethodView):

    def post(self):
        qrcode = Qrcode()

        answer = qrcode.qrcode()

        return jsonify({"Status": "Codigo generado",
                        "image" : answer
                        }), 200




app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'

mongo = PyMongo(app)


class LoginAdminControllers(MethodView):
    def post(self):
        users =  mongo.db.soporteTecnico

        content = request.get_json()
        password = content.get("password")
        print(password)
        
        login_user = users.find_one({'correo' : request.json['correo']})

        
    

        if login_user:
            return jsonify({"Status": "Registro ok",
                    "password_plano": password}), 200

        else:
            print("mal")



class RegisterUserControllers(MethodView):
    def post(self):
        
            users = mongo.db.soporteTecnico
            content = request.get_json()
            correo = content.get("correo")
            password = content.get("password")
            existing_user = users.find_one({'correo' : request.json['correo']})
            print("si esta")
            print(correo)
            print(password)
        

            
            if existing_user is None:
                hashpass = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())
                valor_string = str(hashpass)
                valor = binascii.b2a_base64(hashpass)

                users.insert({'correo' : correo, 'password' : valor})
                session['correo'] = request.json['correo']
                return jsonify({"Status": "Registro ok",
                        "password_plano": password}), 200
            
            else:
                return jsonify({"Status": "Login incorrecto 22"}), 400

'''
Menu de platillo
Responsable Andres Taborda
Methods POST
'''
class MenuControllers(MethodView):
    def get(self):


        data = mongo.db.menu.find({})
        listado_documentos = list(data)

        if data == None:
            data = []

        return jsonify({"transaccion":True,"data":listado_documentos})

class CrearMenuControllers(MethodView):
    def post(self):
        data = request.get_json()
        guardar = mongo.db.menu.insert_one(data)
        return jsonify({"transaccion": True, "mensaje": "Los datos se almacenaron de forma exitosa"})


class MandarMenuControllers(MethodView):
    def post(self):
        
        peticion = Peticion()

        answer = peticion.peticion()

        return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})


'''
Clase Carrito
Responsable Michael Giraldo
Methods POST
'''
class CarritoControllers(MethodView):

    def post(self):
        datos_token = ""
        idMesa = 1
        tokenR = request.headers.get('Authorization').split(" ")
        token = tokenR[1]
       
        datos_token = jwt.decode(token, KEY_TOKEN_AUTH , algorithms=['HS256'])
        # correo = datos_token.get("correo")

        json_req = request.get_json(force=True)
        idPlatillo = json_req["idPlatillo"]
 
        carrito = Carrito()
        
        carrito.idMesa = idMesa
        carrito.idPlatillo = idPlatillo
        
        answer = carrito.Add()

        return jsonify({"Status": "Platillo añadido correctamente",
                        }), 200



