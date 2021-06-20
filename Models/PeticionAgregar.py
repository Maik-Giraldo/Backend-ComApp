#Importacion de Librerias necesarias
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP
import smtplib
from email.mime.text import MIMEText
from flask import jsonify, request, render_template
import json
import os
from PIL import Image
from io import BytesIO  
import base64
import dropbox
import random

'''
Class Peticion
@Methods (Peticion, peticionEditar, PeticionEliminar)
Descripcion: clase en la cual se establecen los metodos para enviar correos por parte del rol del gerente
Responsable: Michael Giraldo, Andres taborda, Juan Leiton
'''
class Peticion():

  

    def __init__(self):
        pass

    """
    @Method peticion
    @param self
    Desciprcion: metodo para enviar una peticion al correo de agregar un platillo
    @return 
    """
    def peticion(self):

        try:
            data = request.get_json()
            data2 = json.dumps(data)
            dataObject = json.loads(data2)
            id_platillo = dataObject['id_platillo']
            platillo = dataObject['platillo']
            descripcion = dataObject['descripcion']
            precio_unitario = dataObject['precio_unitario' ]
            tipo = dataObject['tipo']
            img = dataObject['img']
            img_final = ''
            
            #Validacion si la imagem es (gif, jpeg, png)
            if "data:image/gif;base64," in img:
                img_final = img[22::]

            elif "data:image/jpeg;base64," in img:
                img_final = img[23::]

            elif "data:image/png;base64," in img:
                img_final = img[22::]
            
            else:
                return jsonify({}), 200

            #Guardar imagen en la nube
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
                result = dbx.files_upload(f.read(), '/ComApp/peticion_menu/' + nombre)

            os.remove(nombre_image)

            link = dbx.sharing_create_shared_link(path='/ComApp/peticion_menu/' + nombre)

            link_image = link.url.replace('?dl=0', '?dl=1')

            #Enviar correo de peticion
            subject = 'peticion para agregar'
            archivo = render_template("correo.html", id_platillo = id_platillo, subject = subject, platillo= platillo, descripcion= descripcion, precio_unitario =precio_unitario , tipo= tipo, image= link_image)

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
            msg['To'] = 'comapp.helloworld@gmail.com'
            msg['Subject'] = 'COMAPP - peticion para agregar un nuevo platillo'
            servidor.sendmail(msg['From'] , msg['To'], msg.as_string())

            return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})

        except:

            return jsonify({"transaccion": False, "mensaje": "error"})

    """
    @Method peticionEditar
    @param self
    Desciprcion: metodo para enviar una peticion al correo de editar un platillo
    @return 
    """
    def peticionEditar(self):
        try: 
            data = request.get_json()
            data2 = json.dumps(data)
            dataObject = json.loads(data2)
            id_platillo = dataObject['id_platillo']
            platillo = dataObject['platillo']
            descripcion = dataObject['descripcion']
            precio_unitario = dataObject['precio_unitario' ]
            tipo = dataObject['tipo']

            img = dataObject['img']
            img_final = ''

            #variable para validar si esta cambiando la imagen o esta insertando una nueva
            imagen_cambio = False
            link_image = img

            #Validacion si la imagen es (gif, jpeg, png) 
            if "data:image/gif;base64," in img:
                img_final = img[22::]
                imagen_cambio = True

            if "data:image/jpeg;base64," in img:
                img_final = img[23::]
                imagen_cambio = True

            if "data:image/png;base64," in img:
                img_final = img[22::]
                imagen_cambio = True
            
            #Validacion si esta cambaindo la imagen o es una nueva imagen opara enviar el correo de peticion
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

            if img:

                #Envio del correo de peticion
                subject = 'peticion para editar'
                archivo = render_template("correo.html", id_platillo = id_platillo, subject = subject, platillo= platillo, descripcion= descripcion, precio_unitario =precio_unitario , tipo= tipo, image= link_image  )
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
                msg['To'] = 'comapp.helloworld@gmail.com'
                msg['Subject'] = ' COMAPP - Peticion para editar un platillo'
                servidor.sendmail(msg['From'] , msg['To'], msg.as_string())

                return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})
        except:

            return jsonify({"transaccion": False, "mensaje": "error"})
        
    """
    @Method peticionEliminar
    @param self
    Desciprcion: metodo para enviar una peticion al correo de eliminar un platillo
    @return 
    """
    def peticionEliminar(self):

        try:
            data = request.get_json()
            data2 = json.dumps(data)
            dataObject = json.loads(data2)
            id_platillo = dataObject['id_platillo']
            platillo = dataObject['platillo']
            descripcion = dataObject['descripcion']
            precio_unitario = dataObject['precio_unitario' ]
            tipo = dataObject['tipo']

            #Envio de correo para peticion para eliminar
            subject = 'peticion para Eliminar'
            archivo = render_template("correo.html", id_platillo = id_platillo, subject = subject, platillo= platillo, descripcion= descripcion, precio_unitario =precio_unitario , tipo= tipo)

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
            msg['To'] = 'comapp.helloworld@gmail.com'
            msg['Subject'] = ' COMAPP - Peticion para Eliminar un platillo'
            servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
            return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})

        except:

            return jsonify({"transaccion": False, "mensaje": "error"})

    """
    @Method peticionContacto
    @param self
    Desciprcion: metodo para enviar una peticion al correo de contacto
    @return 
    """
    def peticionContacto(self):

      try:
            data = request.get_json()
            data2 = json.dumps(data)
            dataObject = json.loads(data2)
            asunto = dataObject['asunto']
            nombre = dataObject['nombre']
            correo = dataObject['correo' ]
            descripcion = dataObject['descripcion']
            telefono = dataObject['telefono']

            # Envio de correo para peticion para contacto
            subject = str(asunto)
            archivo = render_template("correoContacto.html", descripcion = descripcion, nombre = nombre, correo= correo, telefono = telefono)

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
            msg['To'] = 'comapp.helloworld@gmail.com'
            msg['Subject'] = asunto
            servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
            return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})

      except:

            return jsonify({"transaccion": False, "mensaje": "error"})