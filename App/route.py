from App.Contoral.User.user import Login, Register, Logout, Echo
from App.Contoral.User.user import LoginByPhone, RegisterByPhone, ForgetPassword
from App.Contoral.User.user import UploadAvatar, Follow, GetAllFollowed, GetAllFollower, UpdateUserInfo


def set_route(api):
    api.add_resource(Echo, "/echo/<input_lines>")
    api.add_resource(Login, "/login")
    api.add_resource(Register, "/register")
    api.add_resource(Logout, "/logout")
    api.add_resource(LoginByPhone, "/loginPhone/<phone_number>")
    api.add_resource(RegisterByPhone, "/registerPhone/<phone_number>")
    api.add_resource(ForgetPassword, "/forgetPassword/<phone_number>")
    api.add_resource(UploadAvatar, "/uploadAvatar")
    api.add_resource(Follow, "/follow")
    api.add_resource(GetAllFollower, "/get_all_follower")
    api.add_resource(GetAllFollowed, "/get_all_followed")
    api.add_resource(UpdateUserInfo, "/update_user_info")