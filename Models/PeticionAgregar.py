#Importacion de Librerias necesarias
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import smtplib
from email.mime.text import MIMEText
from flask import jsonify, request
import json

class Peticion():

    def __init__(self):
        pass

    def peticion(self):
        data = request.get_json()

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