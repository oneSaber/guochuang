from App.Contoral.User.user import Login, Register


def set_route(api):
    api.add_resource(Login, "/login")
    api.add_resource(Register, "/register")
