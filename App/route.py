from App.Contoral.User.user import Login, Register, Logout, Echo
from App.Contoral.User.user import LoginByPhone, RegisterByPhone, ForgetPassword


def set_route(api):
    api.add_resource(Echo, "/echo/<input_lines>")
    api.add_resource(Login, "/login")
    api.add_resource(Register, "/register")
    api.add_resource(Logout, "/logout")
    api.add_resource(LoginByPhone, "/loginPhone/<phone_number>")
    api.add_resource(RegisterByPhone, "/registerPhone/<phone_number>")
    api.add_resource(ForgetPassword, "/forgetPassword/<phone_number>")
