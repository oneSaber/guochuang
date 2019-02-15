from flask_restful import Resource
from flask_restful import reqparse
from App.Contoral import user_common, upload_common


# echo test
class Echo(Resource):
    def get(self, input_lines):
        return input_lines


# login by account and password
class Login(Resource):
    def __init__(self):
        # 参数解析
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("account", type=str)
        self.parser.add_argument("password", type=str)

    def post(self, **kwargs):
        args = self.parser.parse_args()
        result = user_common.login(args.get("account"), args.get("password"))
        if result == -400:
            return {'msg': "password error", 'user_id': 0}, 400
        elif result == -404:
            return {'msg': "no this user!", 'user_id': 0}, 404
        else:
            return {'msg': 'login successful', 'user_id': result}


# login by phone_number
class LoginByPhone(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("phone_number", type=str)
        self.parser.add_argument("identifying_code", type=str)

    def get(self, phone_number):
        res = user_common.login_with_phone(phone_number)
        if res == -404:
            return {'msg': 'no this user'}, 404
        if res == 0:
            return {'msg': '注意接收短信'}, 200
        return {'msg': '已经登陆了', 'user_id': res}, 403

    def post(self, phone_number, identifying_code):
        res = user_common.indent_login_code(phone_number, identifying_code)
        if res == -400:
            return {'msg': '验证码错误，请重新输入'}, 400
        if res == -404:
            return {'msg': '验证码已经过期，请重新申请'}, 404
        else:
            return {'msg': 'login successful', 'user_id': res}


# register by account and password
class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("account", type=str)
        self.parser.add_argument("password", type=str)
        self.parser.add_argument("name", type=str)
        self.parser.add_argument("role", type=str)

    def post(self, **kwargs):
        args = self.parser.parse_args()
        if user_common.check_register(args.get("account")):
            msg, res = user_common.register(args.get("account"), args.get("password"),
                                    args.get("name", None), args.get('role'))
            if res:
                return {'msg': 'register successful'}
            else:
                return {'msg': 'register failure'}
        else:
            return {'msg': 'account had been used'}


# register by phone_number
class RegisterByPhone(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("phone_number", type=str)
        self.parser.add_argument("identifying_code", type=str)

    def get(self, phone_number):
        user_common.send_identifying_code(phone_number)
        return {'msg': '注意接收短信'}

    def post(self, phone_number):
        args = self.parser.parse_args()
        res = user_common.indent_code(args.get('phone_number'), args.get('identifying_code'))
        if res:
            return {'msg': 'register successful'}
        else:
            return {'msg': 'register failure'}, 403


class Logout(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user_id", type=int)

    def post(self, **kwargs):
        args = self.parser.parse_args()
        if user_common.logout(args.get("user_id")):
            return {'msg': 'logout successful'}
        else:
            return {'msg': 'logout failure'}, 403


# 在登陆之后才能被响应, 成功返回一个用户信息的json,失败返回None 和 401
class GetUserInfo(Resource):
    def get(self, user_id):
        if user_common.check_login(user_id):
            print(user_id)
            res = user_common.get_user_info(user_id)
            print(res)
            return {'user_info': res}
        else:
            return None, 401


# forget password
class ForgetPassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("phone_number")
        self.parser.add_argument("account")
        self.parser.add_argument("identifying_code")
        self.parser.add_argument("new_password")

    def get(self, phone_number):
        user_common.lost_password(phone_number)
        return {'msg': "注意接收验证码"}

    def post(self):
        args = self.parser.parse_args()
        res = user_common.change_password(args.get('phone_number'),
                                          args.get('identifying_code'),
                                          args.get('new_password'),
                                          args.get("account", None))
        if res == -400:
            return {'msg': '验证码已经过期'}, 400
        if res == -401:
            return {'msg': "验证码错误"}, 401
        if res == -404:
            return {'msg': '用户不存在'}, 404
        return {'msg': 'login successful', 'user_id': res}


# 上传头像，需要先向服务器申请一个上传的token，token 有效时间为3600s，拿到token后客户端自行上传图片
# 在有效时间内上传完毕把通过回调函数得到的url通过json，post到服务器，如果超时未完成则向服务器报告上传
# 失败, 将会重新发送一个新的token
class UploadAvatar(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('avatar_link', type=str)
        self.parser.add_argument('upload_result', type=str) # successful or failure
        self.parser.add_argument('user_id', type=int)

    def get(self):
        return {'token': upload_common.get_upload_token('avatar')}

    def post(self, **kwargs):
        args = self.parser.parse_args()
        if args.get('upload_result') == 'failure':
            return upload_common.get_upload_token('avatar')
        else:
            res = user_common.set_avatar(args.get('avatar_link'), args.get('user_id'))
            if res == 200:
                return {'msg': 'set avatar_link ok '}, 200
            elif res == -404:
                return {'msg': 'no this user'}, 404
            elif res == -400:
                return {'msg': 'set failure'}, 400


# 更新用户信息，不包括密码，头像链接和角色。
# 一次可以更新1-3个项目, 必须传递user_id
class UpdateUserInfo(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=str)
        self.parser.add_argument('account', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('signed', type=str)

    def post(self, **kwargs):
        args = self.parser.parse_args()
        res = user_common.updateInfo(user_id=args.get('user_id'),
                                     account=args.get('account'),
                                     name=args.get('name'),
                                     signed=args.get('signed'))

        if res == 400:
            return {'msg': 'no user_id'}, 400
        elif res == 404:
            return {'msg': 'no this user'}, 404
        elif res == 403:
            return {'msg': 'upload failure'}, 403
        else:
            return user_common.get_user_info(args.get('user_id')), 200


# 获得用户的所有关注者
class GetAllFollower(Resource):
    def get(self,user_id):
        return {'follower': user_common.all_follower(user_id=user_id)}


# 获得所有关注该用户的user_id
class GetAllFollowed(Resource):
    def get(self, user_id):
        return {'followed': user_common.all_follow(user_id=user_id)}


# 被实现的关注功能
class Follow(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('follower_id', type=int)
        self.parser.add_argument('followed_id', type=int)

    def get(self):
        args = self.parser.parse_args()
        res = user_common.follow_someone(args.get('follower_id'), args.get('followed_id'))
        if res == -200:
            return {'msg': '取消关注成功'}, 200
        elif res == 200:
            return {'msg': '关注成功'}, 200
        elif res == 403:
            return {'msg': '操作失败'}, 403
