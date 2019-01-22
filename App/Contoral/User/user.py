from flask_restful import Resource
from flask_restful import reqparse
from App.Contoral import user_common


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
