#importaciones de librerias y framework
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

#importacion de modelos
from Models.Conexion import * 

#Configuracion en el CORS
CORS(app, resources={
    r"/*": {"origins": "*"},
    r"/*": {
        "origins": ["*"],
        "methods": ["OPTIONS", "POST", "PUT", "GET", "DELETE"],
        "allow_headers": ["Authorization", "Content-Type"],
        }
    })

#importacion de rutas
from Routes.Routes import *

#Reglas de rutas Suport
app.add_url_rule(suport["qrcode"], view_func=suport["qrcodecontrollers"])



if __name__ == '__main__':
    app.run(debug=True,port=5000)