#importaciones de librerias y framework
from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='')

#importacion de modelos
from Models.Conexion import * 

port = int(os.getenv('PORT', 8000))

#Configuracion en el CORS
CORS(app, resources={
    r"/*": {"origins": "*"},
    r"/*": {
        "origins": ["*"],
        "methods": ["OPTIONS", "POST", "PUT", "GET", "DELETE"],
        "allow_headers": ["Authorization", "Content-Type", "id_mesa"],
        }
    })

#importacion de rutas
from Routes.Routes import *

#Reglas de rutas
app.add_url_rule(suport["qrcode"], view_func=suport["qrcodecontrollers"])

app.add_url_rule(user["register_user"], view_func=user["register_user_controllers"])
 
app.add_url_rule(admin["login_admin"], view_func=admin["login_admin_controllers"])

app.add_url_rule(menu["listar_menu"], view_func=menu["listar_menu_controllers"])

app.add_url_rule(crearMenu["crear_menu"], view_func=crearMenu["crear_menu_controllers"])

app.add_url_rule(mandarMenu["mandar_menu"], view_func=mandarMenu["mandar_menu_controllers"])

app.add_url_rule(peticionEditar["peticion_editar"], view_func=peticionEditar["peticion_editar_controllers"])

app.add_url_rule(peticionEliminar["peticion_eliminar"], view_func=peticionEliminar["peticion_eliminar_controllers"])

app.add_url_rule(peticionContacto["peticion_contacto"], view_func=peticionContacto["peticion_contacto_controllers"])

app.add_url_rule(editarMenu["editar_menu"], view_func=editarMenu["editar_menu_controllers"])

app.add_url_rule(eliminarMenu["eliminar_menu"], view_func=eliminarMenu["eliminar_menu_controllers"])

app.add_url_rule(agregarCarrito["agregar_carrito"], view_func=agregarCarrito["agregar_carrito_controllers"])

app.add_url_rule(eliminarCarrito["eliminar_carrito"], view_func=eliminarCarrito["eliminar_carrito_controllers"])

app.add_url_rule(CarritoCompras["carrito_compras"], view_func=CarritoCompras["carrito_compras_controllers"])

app.add_url_rule(ConfirmarPedido["confirmar_pedido"], view_func=ConfirmarPedido["confirmar_pedido_controllers"])

app.add_url_rule(RechazarPedido["rechazar_pedido"], view_func=RechazarPedido["rechazar_pedido_controllers"])

app.add_url_rule(PersonalCocina["personal_cocina"], view_func=PersonalCocina["personal_cocina_controllers"])

app.add_url_rule(IngresarCliente["ingresar_cliente"], view_func=IngresarCliente["ingresar_cliente_controllers"])

app.add_url_rule(ConfirmarCocina["confirmar_cocina"], view_func=ConfirmarCocina["confirmar_cocina_controllers"])

app.add_url_rule(FinalizarCocina["finalizar_cocina"], view_func=FinalizarCocina["finalizar_cocina_controllers"])

app.add_url_rule(RechazarCocina["rechazar_cocina"], view_func=RechazarCocina["rechazar_cocina_controllers"])

app.add_url_rule(FacturaCliente["factura_cliente"], view_func=FacturaCliente["factura_cliente_controllers"])

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    # app.run(host='0.0.0.0', debug=True, port=port)
    app.run(host='0.0.0.0', debug=True, port=5000)