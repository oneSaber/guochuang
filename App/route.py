from App.Contoral.User.user import Login, Register, Logout, Echo
from App.Contoral.User.user import LoginByPhone, RegisterByPhone, ForgetPassword, GetUserInfo
from App.Contoral.User.user import UploadAvatar, Follow, GetAllFollowed, GetAllFollower, UpdateUserInfo


def set_route(api):
    api.add_resource(Echo, "/echo/<input_lines>")
    api.add_resource(Login, "/user/login")
    api.add_resource(Register, "/user/register")
    api.add_resource(Logout, "/user/logout")
    api.add_resource(LoginByPhone, "/user/loginPhone/<phone_number>")
    api.add_resource(RegisterByPhone, "/user/registerPhone/<phone_number>")
    api.add_resource(ForgetPassword, "/user/forgetPassword/<phone_number>")
    api.add_resource(UploadAvatar, "/user/uploadAvatar")
    api.add_resource(Follow, "/user/follow")
    api.add_resource(GetAllFollower, "/user/getAllFollower")
    api.add_resource(GetAllFollowed, "/user/getAllFollowed")
    api.add_resource(GetUserInfo, "/user/getUserInfo/<int:user_id>")
    api.add_resource(UpdateUserInfo, "/user/updateUserInfo")