from Controllers.Controllers import QrCodeControllers ,RegisterUserControllers,LoginAdminControllers, MenuControllers, CrearMenuControllers,MandarMenuControllers 

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