from Controllers.Controllers import QrCodeControllers ,RegisterUserControllers,LoginAdminControllers, MenuControllers, CrearMenuControllers,MandarMenuControllers, EditarMenuControllers, EliminarMenuControllers, AgregarCarritoControllers, EliminarCarritoControllers, CarritoCompras , ConfirmarPedidoControllers,RechazarPedidoControllers, PeticionEditarControllers, PeticionEliminarControllers

suport = {
    "qrcode": "/api/v01/suport/qrcode", "qrcodecontrollers": QrCodeControllers.as_view("qrcode_api")
}


user = {
   "register_user": "/api/v01/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api"),
}

 
admin = {
    "login_admin": "/api/v01/admin/login", "login_admin_controllers": LoginAdminControllers.as_view("login_api"),
}

menu = {
    "listar_menu": "/api/v01/menu/listarMenu", "listar_menu_controllers": MenuControllers.as_view("menu_api"),
}

crearMenu = {
    "crear_menu": "/api/v01/menu/crearMenu", "crear_menu_controllers": CrearMenuControllers.as_view("crearMenu_api"),
}

mandarMenu = {
    "mandar_menu": "/api/v01/menu/mandarMenu", "mandar_menu_controllers": MandarMenuControllers.as_view("mandarMenu_api"),
}

peticionEditar = {
    "peticion_editar": "/api/v01/menu/peticionEditar", "peticion_editar_controllers":PeticionEditarControllers.as_view("peticionEditar_api"),
}

peticionEliminar = {
    "peticion_eliminar": "/api/v01/menu/peticionEliminar", "peticion_eliminar_controllers":PeticionEliminarControllers.as_view("peticionEliminar_api"),
}

editarMenu = {
    "editar_menu": "/api/v01/menu/editarMenu", "editar_menu_controllers": EditarMenuControllers.as_view("editarMenu_api"),
}
eliminarMenu = {
    "eliminar_menu": "/api/v01/menu/eliminarMenu", "eliminar_menu_controllers": EliminarMenuControllers.as_view("eliminarMenu_api"),
}

agregarCarrito = {
    "agregar_carrito": "/api/v01/menu/agregarCarrito", "agregar_carrito_controllers": AgregarCarritoControllers.as_view("agregarCarrito_api"),
}

eliminarCarrito = {
    "eliminar_carrito": "/api/v01/menu/eliminarCarrito", "eliminar_carrito_controllers": EliminarCarritoControllers.as_view("eliminarCarrito_api"),
}

CarritoCompras = {
    "carrito_compras": "/api/v01/menu/carritocompras", "carrito_compras_controllers": CarritoCompras.as_view("carrito_compras")
}


ConfirmarPedido = {
     "confirmar_pedido": "/api/v01/menu/confirmarPedido", "confirmar_pedido_controllers": ConfirmarPedidoControllers.as_view("confirmar_pedido")

}

RechazarPedido = {
     "rechazar_pedido": "/api/v01/menu/rechazarPedido", "rechazar_pedido_controllers": RechazarPedidoControllers.as_view("rechazar_pedido")
}