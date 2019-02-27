from App import db, cache
from App.Models.models import Account, Follow
from datetime import datetime
from faker import Faker


class User:
    def __init__(self):
        self.LOGIN_CACHE = "LOGIN_USER"
        self.LIVE_TIME = 7  # day
        self.ROLE_LEVEL = {'normal_user': 1, 'vip_user': 2, 'creator': 3, 'admin': 4}
        self.fake = Faker()

    # 检查提交注册的账号是否合法
    def check_account(self,account):
        if 8 <len(account)< 32:
            return True
        else:
            return False

    # 随机生成6位数字验证码
    def create_check(self):
        import random
        res = ""
        for i in range(6):
            res += random.randint(0, 9)
        return res

    # 注册程序,username 可以先置为空，如果为空用account代替
    def register(self, user_account, user_password, user_name=None, user_role='normal_user'):
        if not self.check_account(user_account):
            return ('account should between 8 to 32', False)
        if not self.check_register(user_account):
            return ('had register', False)
        if user_name is None:
            user_name = user_account
        new_account = Account(account=user_account, password=user_password,name=user_name, role=user_role)
        try:
            db.session.add(new_account)
            db.session.commit()
            return ('register successful',True)
        except Exception as e:
            print(e)
            db.session.rollback()
            return ('bad server',False)

    # register by phone number
    def send_identifying_code(self, phone_number):
        identifying_code = self.create_check()
        # 生存时间为10分钟
        if cache.exists(phone_number):
            cache.delete(phone_number)
        cache.set(phone_number, identifying_code, ex=60*10)
        # send checking_password to user's phone

    # checking identifying code
    def indent_code(self, phone_number, identifying_code):
        store_code = cache.get(phone_number)
        if store_code is None or store_code != identifying_code:
            return False
        else:
            if cache.exists(phone_number):
                cache.delete(phone_number)
            new_user = Account(account=phone_number, password=None,
                               name=self.fake.name(), role="normal_user")
            db.session.add(new_user)
            db.session.commit()
            return True

    # login_with_phone
    def login_with_phone(self, phone_number):
        login_user = Account.query.filter_by(account=phone_number).first()
        if login_user is None:
            return -404
        if self.check_login(login_user.user_id):
            cache.hset(self.LOGIN_CACHE, login_user.user_id, datetime.timestamp(datetime.now()))
            return login_user.user_id
        login_code = self.create_check()
        # send_code for user
        cache.set(name=phone_number, value=login_code, ex=60*10)
        return 0

    # 验证登陆验证码
    def indent_login_code(self, phone_number, identifying_code):
        login_code = cache.get(phone_number)
        if login_code is None:
            return -404
        elif login_code != identifying_code:
            return -400
        else:
            if cache.exists(phone_number):
                cache.delete(phone_number)
            login_user = Account.query.filter_by(account=phone_number).first()
            cache.hset(self.LOGIN_CACHE, login_user.user_id, datetime.timestamp(datetime.now()))
            return login_user.user_id

    # 登陆程序, 成功则返回用户id, 失败则返回错误信息 -400, 用户不存在则返回 -404
    def login(self, user_account, user_password):
        login_user = Account.query.filter_by(account=user_account).first()
        if login_user is None:
            return -404
        if self.check_login(login_user.user_id):
            # 更新登陆时间
            cache.hset(self.LOGIN_CACHE, login_user.user_id,datetime.timestamp(datetime.now()))
            return login_user.user_id,
        # 密码正确 登陆成功
        if login_user.password == user_password:
            print(login_user.password, user_password)
            res = cache.hset(self.LOGIN_CACHE, login_user.user_id, datetime.timestamp(datetime.now()))
            print(res)
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
        last_login_timestamp = datetime.fromtimestamp(float(last_login_timestamp))
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
    def check_register(self, user_account):
        user = Account.query.filter_by(account=user_account).first()
        if user is not None:
            return False
        else:
            return True

    # 检查用户的某项请求是否具有相应的权限
    def check_permission(self, user_id, min_role):
        user = Account.query.filter_by(user_id=user_id).first()
        if user is None:
            return False
        if self.ROLE_LEVEL[user.role] >= self.ROLE_LEVEL[min_role]:
            return True
        else:
            return False

    # 使用user_id 获取用户信息,得到account, user_name, avatar_link, signed
    def get_user_info(self, user_id):
        user = Account.query.filter_by(user_id=user_id).first()
        print(user)
        if user is not None:
            return {
                'account': user.account,
                'name': user.name,
                'avatar_link': user.avatar_link,
                'signed': user.signed
            }
        else:
            return None

    # 找回密码，发送验证码到指定手机
    def lost_password(self, phone_number):
        identifying_code = self.create_check()
        # send to phone
        if cache.exists(phone_number):
            cache.delete(phone_number)
        cache.set(name=phone_number, value=identifying_code, ex=60*10)

    # change_password, 如过改变成功直接登陆并返回user_id
    def change_password(self, phone_number, identifying_code, new_password, account=None):
        code = cache.get(phone_number)
        if code is None:
            return -400
        if code != identifying_code:
            return -401
        else:
            if cache.exists(phone_number):
                cache.delete(phone_number)
            user = None
            if account is None:
                user = Account.query.filter_by(account=phone_number).first()
            else:
                user = Account.query.filter_by(account=account).first()
            if user is None:
                return -404
            else:
                user.password = new_password
                db.session.add(user)
                db.session.commit()
                cache.hset(self.LOGIN_CACHE, user.user_id, datetime.timestamp(datetime.now()))
                return user.user_id

    def set_avatar(self, avatar_link, user_id):
        user = Account.query.filter_by(user_id=user_id).first()
        if user is None:
            return -404
        import Config
        user.avatar_link = Config.TestingConfig.AVATAR_NAMESPACE + avatar_link
        db.session.add(user)
        try:
            db.session.commit()
            return 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return -400

    # 更新用户信息
    def updateInfo(self, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            return 400
        else:
            user = Account.query.filter_by(user_id=user_id).first()
            if user is None:
                return 404
            else:
                account = kwargs.get('account', user.account)
                name = kwargs.get('name', user.name)
                signed = kwargs.get('signed', user.signed)
                user.account = account
                user.name = name
                user.signed = signed
                try:
                    db.session.add(user)
                    db.session.commit()
                    return 200
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return 403

    # 判断是否A follow B
    def had_follow(self, follower_id, followed_id):
        follow = Follow.query.filter(Follow.follower == follower_id and Follow.followed_id == followed_id).first()
        return follow

    # 关注/取消关注某个用户
    def follow_someone(self,follower_id, followed_id):
        follow = self.had_follow(follower_id,followed_id)
        if follow is not None:
            # 已经关注了，那就是取消关注
            try:
                db.session.delete(follow)
                db.session.commit()
                return -200
            except Exception as e:
                print(e)
                return 403
        else:
            # 没有关注那就关注吧
            new_follow = Follow(follower=follower_id, followed=followed_id)
            try:
                db.session.add(new_follow)
                db.session.commit()
                return 200
            except Exception as e:
                print(e)
                return 403

    # 获取用户的所有关注对象的user_id
    def all_follow(self, user_id):
        all_follow = Follow.query.filter_by(follower=user_id).all()
        return [follow.followed for follow in all_follow]

    # 获取所有关注该用户的user_id
    def all_follower(self, user_id):
        all_follower = Follow.query.filter_by(followed=user_id).all()
        return [follow.follower for follow in all_follower]
