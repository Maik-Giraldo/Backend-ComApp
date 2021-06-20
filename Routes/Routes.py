#Importacion controladores
from Controllers.Controllers import QrCodeControllers ,RegisterUserControllers,LoginAdminControllers, MenuControllers, CrearMenuControllers,MandarMenuControllers, EditarMenuControllers, EliminarMenuControllers, AgregarCarritoControllers, EliminarCarritoControllers, CarritoCompras , ConfirmarPedidoControllers,RechazarPedidoControllers,PeticionEditarControllers,PeticionEliminarControllers,FacturasControllers, IngresarClienteControllers, ConfirmarCocinaControllers, FinalizarCocinaControllers, RechazarCocinaControllers,FacturaClienteControllers, PeticionContactoControllers

#Ruta soporte tecnico codigo qr
suport = {
    "qrcode": "/api/v01/suport/qrcode", "qrcodecontrollers": QrCodeControllers.as_view("qrcode_api")
}

#Ruta registro usuario
user = {
   "register_user": "/api/v01/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api"),
}

#Ruta login
admin = {
    "login_admin": "/api/v01/admin/login", "login_admin_controllers": LoginAdminControllers.as_view("login_api"),
}

#Ruta listar menu
menu = {
    "listar_menu": "/api/v01/menu/listarMenu", "listar_menu_controllers": MenuControllers.as_view("menu_api"),
}

#Ruta crear menu
crearMenu = {
    "crear_menu": "/api/v01/menu/crearMenu", "crear_menu_controllers": CrearMenuControllers.as_view("crearMenu_api"),
}

#Ruta peticion
mandarMenu = {
    "mandar_menu": "/api/v01/menu/mandarMenu", "mandar_menu_controllers": MandarMenuControllers.as_view("mandarMenu_api"),
}

#Ruta peticion editar menu
peticionEditar = {
    "peticion_editar": "/api/v01/menu/peticionEditar", "peticion_editar_controllers":PeticionEditarControllers.as_view("peticionEditar_api"),
}

#Ruta peticion eliminar menu
peticionEliminar = {
    "peticion_eliminar": "/api/v01/menu/peticionEliminar", "peticion_eliminar_controllers":PeticionEliminarControllers.as_view("peticionEliminar_api"),
}

#Ruta peticion contacto menu
peticionContacto = {
    "peticion_contacto": "/api/v01/menu/peticionContacto", "peticion_contacto_controllers":PeticionContactoControllers.as_view("peticionContacto_api"),
}

#Ruta editar menu
editarMenu = {
    "editar_menu": "/api/v01/menu/editarMenu", "editar_menu_controllers": EditarMenuControllers.as_view("editarMenu_api"),
}

#Ruta eliminar menu
eliminarMenu = {
    "eliminar_menu": "/api/v01/menu/eliminarMenu", "eliminar_menu_controllers": EliminarMenuControllers.as_view("eliminarMenu_api"),
}

#Ruta agregar carrito
agregarCarrito = {
    "agregar_carrito": "/api/v01/menu/agregarCarrito", "agregar_carrito_controllers": AgregarCarritoControllers.as_view("agregarCarrito_api"),
}

#Ruta eliminar carrito
eliminarCarrito = {
    "eliminar_carrito": "/api/v01/menu/eliminarCarrito", "eliminar_carrito_controllers": EliminarCarritoControllers.as_view("eliminarCarrito_api"),
}

#Ruta carrito compras
CarritoCompras = {
    "carrito_compras": "/api/v01/menu/carritocompras", "carrito_compras_controllers": CarritoCompras.as_view("carrito_compras")
}

#Ruta confirmar pedido
ConfirmarPedido = {
     "confirmar_pedido": "/api/v01/menu/confirmarPedido", "confirmar_pedido_controllers": ConfirmarPedidoControllers.as_view("confirmar_pedido")

}

#Ruta rechazar pedido
RechazarPedido = {
     "rechazar_pedido": "/api/v01/menu/rechazarPedido", "rechazar_pedido_controllers": RechazarPedidoControllers.as_view("rechazar_pedido")
}

#Ruta personal cocina
PersonalCocina = {
     "personal_cocina": "/api/v01/menu/personalcocina", "personal_cocina_controllers": FacturasControllers.as_view("personal_cocina")
}

#Ruta ingresar cliente
IngresarCliente = {
     "ingresar_cliente": "/api/v01/menu/ingresarCliente", "ingresar_cliente_controllers": IngresarClienteControllers.as_view("ingresar_cliente")
}

#Ruta confirmar cocina
ConfirmarCocina = {
     "confirmar_cocina": "/api/v01/menu/confirmarCocina", "confirmar_cocina_controllers": ConfirmarCocinaControllers.as_view("confirmar_cocina")
}

#Ruta finalizar cocina
FinalizarCocina = {
     "finalizar_cocina": "/api/v01/menu/finalizarCocina", "finalizar_cocina_controllers": FinalizarCocinaControllers.as_view("finalizar_cocina")
}

#Ruta rechazar cocina
RechazarCocina = {
     "rechazar_cocina": "/api/v01/menu/rechazarCocina", "rechazar_cocina_controllers": RechazarCocinaControllers.as_view("rechazar_cocina")
}

#Ruta facturar cliente
FacturaCliente = {
     "factura_cliente": "/api/v01/menu/facturaCliente", "factura_cliente_controllers": FacturaClienteControllers.as_view("factura_cliente")
}