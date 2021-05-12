#Importacion de Librerias necesarias
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import smtplib
from email.mime.text import MIMEText
from flask import jsonify, request, render_template
import json

class Peticion():

    def __init__(self):
        pass

    def peticion(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['id_platillo']
        platillo = dataObject['platillo']
        descripcion = dataObject['descripcion']
        precio_unitario = dataObject['precio_unitario' ]
        tipo = dataObject['tipo']

        subject = 'peticion para agregar'
        archivo = render_template("correo.html", id_platillo = id_platillo, subject = subject, platillo= platillo, descripcion= descripcion, precio_unitario =precio_unitario , tipo= tipo  )

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
        mensaje = archivo
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = 'felipetabordasanchez@gmail.com'
        msg['Subject'] = 'COMAPP - peticion para agregar un nuevo platillo'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())

    def peticionEditar(self):
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['id_platillo']
        platillo = dataObject['platillo']
        descripcion = dataObject['descripcion']
        precio_unitario = dataObject['precio_unitario' ]
        tipo = dataObject['tipo']

        subject = 'peticion para editar'
        archivo = render_template("correo.html", id_platillo = id_platillo, subject = subject, platillo= platillo, descripcion= descripcion, precio_unitario =precio_unitario , tipo= tipo  )

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
        mensaje = archivo
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = 'felipetabordasanchez@gmail.com'
        msg['Subject'] = ' COMAPP - Peticion para editar un platillo'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())

    def peticionEliminar(self):
 
        data = request.get_json()
        data2 = json.dumps(data)
        dataObject = json.loads(data2)
        id_platillo = dataObject['id_platillo']
        platillo = dataObject['platillo']
        descripcion = dataObject['descripcion']
        precio_unitario = dataObject['precio_unitario' ]
        tipo = dataObject['tipo']

        subject = 'peticion para Eliminar'
        archivo = render_template("correo.html", id_platillo = id_platillo, subject = subject, platillo= platillo, descripcion= descripcion, precio_unitario =precio_unitario , tipo= tipo  )

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
        mensaje = archivo
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = 'felipetabordasanchez@gmail.com'
        msg['Subject'] = ' COMAPP - Peticion para Eliminar un platillo'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())