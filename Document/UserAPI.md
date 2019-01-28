# User API 
version 1.0

## register 
url: http://xxxx/user/register

method: post

注释：使用账号和密码登陆，用户填写account，password选项，name 选填
role 是 客户端填，默认为normal_user

args:{
    
    "account":  // 用户账户
    "password": // 登陆密码
    "name":     // 用户昵称
    "role":     // 用户角色 范围[normal_user, vip_user, creator, admin]，不同角色有不同权限
 }   
return：

200，{'msg': 'register successful'}

200, {"msg": "register failure"}

200, {"msg": "account had been used"}


## login
url = http://xxx/user/login

method = post

注释： 使用账号密码登陆

args:{
   
   "account": // 用户账户
   
   "password": // 用户密码

}

return:

200 {'msg': 'login successful', 'user_id': }

400 {'msg': "password error", 'user_id': 0}

404 {'msg': "no this user!", 'user_id': 0}


## logout

url = http://xxx/user/logout

method = post

args:{
    
    "user_id": // 用户的id，会在登陆时得到
}

return:

200 {'msg': 'logout successful'}

403 {'msg': 'logout failure'}


## registerPhone

url: http://xxx//user/registerPhone/<phone_number>

注释：通过手机号注册账户，有get 和 post两个方法

method: GET

在url中带入phone_number, 服务器会自动向用户发送含有验证码的短信，并回复客户端，验证码有效时间为10分钟

return :

{'msg': '注意接收短信'}

method: POST

在url 中带入phone_number，但还需要再json中传入phone_number
注册成功时，用户账户就是电话号码，密码不设，不自动登陆

args:{

    "phone_number":
    "identifying_code": // 用户收到的六位验证码
}

return:

200, {'msg': 'register successful'}

403, {'msg': 'register failure'}


## loginPhone

基本和注册相同，通过get 方法向用户发送验证码，通过post 方法向服务器验证验证码，成功登陆返回user_id

url: /user/loginPhone/<phone_number>

method: GET

return:

404, {'msg': 'no this user'}

200, {'msg': '注意接收短信'}

403, {'msg': '已经登陆了', 'user_id': res}


method: POST

args:{

    "phone_number":
    "identifying_code"
}

return: 

400, {'msg': '验证码错误，请重新输入'}

404, {'msg': '验证码已经过期，请重新申请'}
200, {'msg': 'login successful', 'user_id': }

## forgetPassword

url: http://xxx/user/forgetPassword/<phone_number>

注释： 和上面两个一样

method: GET

return: 

200, {'msg': "注意接收验证码"}

method: POST

args:
{

    "phone_number":
    "account": // 如果时手机注册这条为phone_number
    "identifying":
    "new_password":    
}

return:

200, {'msg': 'login successful', 'user_id': res}

404, {'msg': '用户不存在'}

401, {'msg': "验证码错误"}

400, {'msg': '验证码已经过期'}