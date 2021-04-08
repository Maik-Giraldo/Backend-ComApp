from flask.views import MethodView
import json
from flask import jsonify, request
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
from Models.Qrcode import Qrcode




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