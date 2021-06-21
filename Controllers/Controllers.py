#Importacion de librerias y frameworks necesarios
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
from Models.Qrcode import Qrcode
from Models.Conexion import * 
from Models.PeticionAgregar import Peticion
from Models.Carrito import Carrito
from Models.CrudMenu import CrudMenu
from Models.PersonalCocina import PersonalCocina

#inicializacion de clases importadas
crudMenu = CrudMenu()
peticion = Peticion()
carrito = Carrito()
personalCocina = PersonalCocina()

#Conexion con mongoDB
app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

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

'''
Clase login
Responsable Juan Camilo Leiton
Methods POST
'''
class LoginAdminControllers(MethodView):
    def post(self):
        users = mongo.db.usuarios
        correo = request.get_json()['correo']
        password = request.get_json()['password']
        result = ""
        response = users.find_one({'correo': correo})

        if response:
            if bcrypt.check_password_hash(response['password'], password):

                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1000), 'correo': response['correo'],'rol': response['rol']}, KEY_TOKEN_AUTH , algorithm='HS256')
                return jsonify({"Status": "Login exitoso", "token": str(encoded_jwt),'correo': response['correo'] , 'rol': response['rol'] }), 200    
                
            else:
                return jsonify({"error":"Invalid username and password"}),400
        else:
            return jsonify({"error":"Invalid username and password"}),400
        return result 

'''
Clase Register
Responsable Juan Camilo Leiton
Methods POST
'''
class RegisterUserControllers(MethodView):
    def post(self):
        users = mongo.db.usuarios
        existing_user = users.find_one({'correo' : request.json['correo']})
        correo = request.get_json()['correo']
        rol = request.get_json()['rol']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        
        #Inserción a la base de datos si es usuario no existe
        if existing_user is None:
            user_id = users.insert({
                'correo': correo,
                'password': password,
                'rol':rol  
            })
            new_user = users.find_one({'_id': user_id})
            result = {'correo': new_user['correo'] + ' registered'}
            return jsonify({'result' : result}),200  
        return jsonify("el correo ya esta"),400

'''
Clase Menu
Responsable Andres Taborda
Methods GET
'''
class MenuControllers(MethodView):
    def get(self):
        answer =  crudMenu.mostrar()
        return jsonify({"transaccion":True,"data":answer})

'''
Clase Facturas
Responsable Andres Taborda
Methods GET
'''
class FacturasControllers(MethodView):
    def get(self):
        answer =  personalCocina.GetFacturas()
        return jsonify({"transaccion":True,"data":answer})

'''
Menu de platillo
Responsable Andres Taborda
Methods GET
'''
class CarritoCompras(MethodView):
    def get(self):
        id_mesa = int(request.headers.get('id_mesa').split(" ")[1])
        crudMenu.id_mesa = id_mesa
        answer =  crudMenu.mostrarcarrito()
        return jsonify({"transaccion":True,"data":answer})

'''
Clase Confirmar Pedido
Responsable Juan Camilo Leiton
Methods POST
'''
class ConfirmarPedidoControllers(MethodView):
    def post(self):
        answer =  carrito.ConfirmarPedido()
        return(answer)

'''
Clase Rechazar Pedido
Responsable Juan Camilo Leiton
Methods POST
'''
class RechazarPedidoControllers(MethodView):
    def post(self):
        answer = carrito.RechazarPedido()

        return jsonify({"transaccion": True, "mensaje": "rechazar el pedido de forma exitosa"}),200

'''
Clase Crear Menu
Responsable Juan Camilo Leiton
Methods POST
'''
class CrearMenuControllers(MethodView):
    def post(self):
        
        answer = crudMenu.crear()
        return(answer)

'''
Clase Mandar Menu
Responsable Andres Taborda
Methods POST
'''
class MandarMenuControllers(MethodView):
    def post(self):
        answer = peticion.peticion()
        return (answer)

'''
Clase Peticion Editar
Responsable Andres Taborda
Methods POST
'''
class PeticionEditarControllers(MethodView):
    def post(self):
        answer = peticion.peticionEditar()
        return (answer)

'''
Clase Peticion Eliminar
Responsable Andres Taborda
Methods POST
'''
class PeticionEliminarControllers(MethodView):
    def post(self):
        answer = peticion.peticionEliminar()
        return (answer)

'''
Clase Peticion Contacto
Responsable Andres Taborda
Methods POST
'''
class PeticionContactoControllers(MethodView):
    def post(self):
        answer = peticion.peticionContacto()
        return (answer)

'''
Clase Editar Menu
Responsable Andres Taborda
Methods PUT
'''
class EditarMenuControllers(MethodView):
    def put(self):
        answer = crudMenu.actualizar()

        return (answer)

'''
Clase Eliminar Menu
Responsable Andres Taborda
Methods POST
'''
class EliminarMenuControllers(MethodView):
    def post(self):
        answer = crudMenu.eliminar()

        return (answer) 
        
'''
Clase Agregar Carrito
Responsable Michael Giraldo
Methods POST
'''
class AgregarCarritoControllers(MethodView):
    def post(self):
        answer = carrito.Agregar()
        return (answer)

'''
Clase Eliminar Carrito
Responsable Juan Camilo Leiton
Methods POST
'''
class EliminarCarritoControllers(MethodView):
    def post(self):
        answer = carrito.Eliminar()
        return (answer)

'''
Clase Contador Carrito
Responsable Andres Taborda
Methods GET 
'''
class ContadorCarritoControllers(MethodView):
    def get(self):
        answer = carrito.ContadorCarrito()
        return (answer)

'''
Clase Ingresar Cliente
Responsable Andres Taborda
Methods POST
'''
class IngresarClienteControllers(MethodView):
    def post(self):
        answer = carrito.IngresarCliente()
        return answer

'''
Clase COnfirmar Cocina
Responsable Andres Taborda
Methods PUT
'''
class ConfirmarCocinaControllers(MethodView):
    def put(self):
        answer = personalCocina.ConfirmarCocina()
        return answer

'''
Clase Finalizar Cocina
Responsable Andres Taborda
Methods PUT
'''
class FinalizarCocinaControllers(MethodView):
    def put(self):
        answer = personalCocina.FinalizarCocina()
        return answer

'''
Clase Rechazar Cocina
Responsable Andres Taborda
Methods PUT
'''
class RechazarCocinaControllers(MethodView):
    def put(self):
        answer = personalCocina.RechazarCocina()
        return answer

'''
Clase Factura Cliente
Responsable Andres Taborda
Methods GET
'''
class FacturaClienteControllers(MethodView):
    def get(self):
        answer = personalCocina.FacturaCliente()
        return jsonify({"transaccion":True,"data":answer})