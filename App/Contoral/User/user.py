from flask_restful import Resource
from flask_restful import reqparse
from App.Contoral import user_common


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

    def put(self, **kwargs):
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
        return {'msg': '已经登陆了', 'user_id': res}

    def put(self, phone_number, identifying_code):
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

    def put(self, **kwargs):
        args = self.parser.parse_args()
        if user_common.check_account(args.get("account")):
            if user_common.register(args.get("account"), args.get("password"),
                                    args.get("name", None), args.get('role')):
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

    def put(self):
        args = self.parser.parse_args()
        res = user_common.indent_code(args.get('phone_number'), args.get('identifying_code'))
        if res:
            return {'msg': 'register successful'}
        else:
            return {'msg': 'register failure'}


class Logout(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user_id", type=int)

    def put(self, **kwargs):
        args = self.parser.parse_args()
        if user_common.logout(args.get("user_id")):
            return {'msg': 'logout successful'}
        else:
            return {'msg': 'logout failure'}


# 在登陆之后才能被响应, 成功返回一个用户信息的json,失败返回None 和 401
class GetUserInfo(Resource):

    def get(self, user_id):
        if user_common.check_login(user_id):
            return user_common.get_user_info(user_id)
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

    def put(self):
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
