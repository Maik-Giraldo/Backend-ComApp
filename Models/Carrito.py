#Importacion conexion
from Models.Conexion import *

#Clase agregar
class Carrito():
    def __init__(self, idMesa, idPlatillo):
    
        self.idMesa = 1
        self.idPlatillo = idPlatillo
    

    def add(self):
        data = {
            "id_mesa": self.idMesa,
            "id_platillo": self.id_platillo 
        }
        data = json.dumps(data)
        res = mongo.db.carrito.insert(data)