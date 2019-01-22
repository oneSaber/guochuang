from App import db, cache
from App.Models.models import Account
from datetime import datetime


class User:
    def __init__(self):
        self.LOGIN_CACHE = "LOGIN_USER"
        self.LIVE_TIME = 7  # day

    # 注册程序,username 可以先置为空，如果为空用account代替
    def register(self, user_account, user_password, user_name=None, user_role='normal_user'):
        if self.check_account(user_account):
            if user_name is None:
                user_name = user_account
            new_user = Account(account=user_account, password=user_password, name=user_name, role=user_role)
            try:
                db.session.add(new_user)
                db.session.commit()
                return True
            except Exception as e:
                print(e)
                return False

    # 登陆程序, 成功则返回用户id, 失败则返回错误信息 -400, 用户不存在则返回 -404
    def login(self, user_account, user_password):
        login_user = Account.query.filter_by(account=user_account).first()
        if login_user is None:
            return -404
        if self.check_login(login_user.user_id):
            # 更新登陆时间
            cache.hset(self.LOGIN_CACHE, login_user.user_id,datetime.timestamp(datetime.now()))
            return login_user.user_id
        # 密码正确 登陆成功
        if login_user.password == user_password:
            cache.hset(self.LOGIN_CACHE, login_user.user_id, datetime.timestamp(datetime.now()))
            return login_user.user_id
        elif login_user.password != user_password:
            return -400

    # 通过用户id检查用户是否登陆或者登陆信息是否有效
    # False 表示没有登陆信息 或者登陆信息已经超时
    def check_login(self,user_id):
        now = datetime.now()
        last_login_timestamp = cache.hget(self.LOGIN_CACHE, user_id)
        if last_login_timestamp is None:
            return False
        last_login_timestamp = datetime.fromtimestamp(last_login_timestamp)
        delta_time = now-last_login_timestamp
        # 登陆信息超时
        # 清除掉相关登陆信息然后返回False
        if delta_time.days > self.LIVE_TIME:
            cache.hdel(self.LOGIN_CACHE, user_id)
            return False
        else:
            return True

    # 推出登陆,接收user_id,删除成功返回True,没有登陆返回False
    def logout(self, user_id):
        if self.check_login(user_id):
            cache.hdel(self.LOGIN_CACHE, user_id)
            return True
        else:
            return False

    # 检查用户账户(Account)是否已经被注册, 被注册返回False,未被注册返回True
    def check_account(self, user_account):
        user = Account.query.filter_by(account=user_account).first()
        if user is not None:
            return False
        else:
            return True
