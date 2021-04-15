from flask.views import MethodView
from flask import Flask, jsonify, request , session
import json
from flask import jsonify, request
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
from Models.Qrcode import Qrcode
from Models.Conexion import * 
import bcrypt
from flask_bcrypt import Bcrypt 
import binascii
from app import app
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import smtplib
from email.mime.text import MIMEText

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




app.config["MONGO_URI"]='mongodb://localhost/comApp'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


class LoginAdminControllers(MethodView):
    def post(self):
        users = mongo.db.usuarios
        correo = request.get_json()['correo']
        password = request.get_json()['password']
        result = ""

        response = users.find_one({'correo': correo})
    # 'correo': response['correo']


        if response:
            if bcrypt.check_password_hash(response['password'], password):
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1000), 'correo': response['correo']}, KEY_TOKEN_AUTH , algorithm='HS256')
                return jsonify({"Status": "Login exitoso", "token": str(encoded_jwt),'correo': response['correo']}), 200    
                
            else:
                return jsonify({"error":"Invalid username and password"}),400
        else:
            return jsonify({"error":"Invalid username and password"}),400
        return result 




class RegisterUserControllers(MethodView):
    def post(self):
        
        users = mongo.db.usuarios
        existing_user = users.find_one({'correo' : request.json['correo']})
        correo = request.get_json()['correo']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        
        if existing_user is None:
            user_id = users.insert({
            
                'correo': correo,
                'password': password,
                
            })

            new_user = users.find_one({'_id': user_id})

            result = {'correo': new_user['correo'] + ' registered'}

            return jsonify({'result' : result}),200  

        return jsonify("el correo ya esta"),400

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
        # print("hola")
        data = request.get_json()
        # mensaje = MIMEMultipart("plain")
        # mensaje["From"] = "felipetabordasanchez@outlook.es"
        # mensaje["To"] = "felipetabordasanchez@gmail.com"
        # mensaje["Subject"] = "nuevo platillo"
        # mensaje.attach(data)
        # smtp = SMTP("smtp.live.com")
        # smtp.starttls()
        # smtp.login("felipetabordasanchez@outlook.es", "qawsed123")
        # smtp.sendmail("felipetabordasanchez@outlook.es", "felipetabordasanchez@gmail.com", mensaje.as_string())
        # smtp.quit()

        
        proveedor_correo = 'smtp.live.com: 587'
        remitente = 'felipetabordasanchez@outlook.es'
        password = 'qawsed123'
        #conexion a servidor
        servidor = smtplib.SMTP(proveedor_correo)
        servidor.starttls()
        servidor.ehlo()
        #autenticacion
        servidor.login(remitente, password)
        #mensaje 
        mensaje = json.dumps(data)
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = 'felipetabordasanchez@gmail.com'
        msg['Subject'] = 'peticion nuevo platillo'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())


        return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})
        



