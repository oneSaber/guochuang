# User API 
version 1.0

## register 
url: http://xxxx/register

method: put

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
