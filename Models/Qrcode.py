#Importacion de librerias
import qrcode
from PIL import Image
from flask import jsonify, request
import dropbox
import random
import os

#Clase qrcode
class Qrcode():
    
    '''
    Method qrcode
    @param self
    @return
    Responsable: Michael Giraldo
    '''

    def __init__(self):
        self.url = ''
        self.nombre = ''
    

    def qrcode(self):

        content = request.get_json()

        url = content.get('id_mesa')

        nombre_json = content.get('nombre')

        key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+%$'
        
        string_random = ''.join(random.sample(key, 64))

        nombre = string_random + nombre_json + '.jpg'

        im = qrcode.make(url)

        print(im)

        # file_image = Image.open(im)

        im.save(nombre)

        result = ''

        dbx = dropbox.Dropbox('i55bkV3doxoAAAAAAAAAAZHHYiUBwkXoHtTHt-S-1R7WmzjiR3CF1qH3LydQ4WEA')

        with open(nombre, 'rb') as f:
            result = dbx.files_upload(f.read(), '/ComApp/Qrcode/' + nombre)

        os.remove(nombre)

        link = dbx.sharing_create_shared_link(path='/ComApp/Qrcode/' + nombre)

        link_image = link.url.replace('?dl=0', '?dl=1')

        print(link_image)

        return link_image