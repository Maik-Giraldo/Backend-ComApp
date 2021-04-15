#Importacion conexion
from Models.Conexion import *

#Clase agregar
class Carrito():
    def __init__(self, idMesa, idPlatillo):
    
        self.idMesa = 1
        self.idPlatillo = idPlatillo
    

    def Add(self):
        data = {
            "id_mesa": self.idMesa,
            "id_platillo": self.idPlatillo 
        }
        data = json.dumps(data)
        res = mongo.db.carrito.insert(data)