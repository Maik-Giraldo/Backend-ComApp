from Controllers.Controllers import QrCodeControllers ,RegisterUserControllers,LoginAdminControllers

suport = {
    "qrcode": "/api/v01/suport/qrcode", "qrcodecontrollers": QrCodeControllers.as_view("qrcode_api")
}


user = {
   "register_user": "/api/v01/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api"),
}

 
admin = {
    "login_admin": "/api/v01/admin/login", "login_admin_controllers": LoginAdminControllers.as_view("login_api"),
}