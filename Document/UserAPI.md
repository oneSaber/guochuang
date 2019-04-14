# User API 
version 1.0

## register (可用)
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


## login (可用)
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


## logout （可用）

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

## uploadAvatar

url: http://xxx/user/uploadAvatar

注释：上传头像，需要先向服务器申请一个上传的token，token 有效时间为3600s，

拿到token后客户端自行上传图片。有效时间内上传完毕把通过回调函数得到的url通过json，

post到服务器，如果超时未完成则向服务器报告上传失败, 将会重新发送一个新的token

method: GET

return: 

200, {'token': upload_common.get_upload_token('avatar'}

method: POST

args:
{

    "avatar_link":
    "upload_result"
    "user_id":   
}

return:

200, {'msg': 'set avatar_link ok '}

404, {''msg': 'no this user'}

400, {'msg': 'set failure'}

## Follow

注释：被实现的关注功能

url: http://xxx/user/follow

method: GET

args:
{

    "follower_id":
    "followed_id"
}

return:

200, {'msg': '取消关注成功'}

200, {'msg': '关注成功}

403, {'msg': '操作失败'}

## GetAllFollower

url: http://xxx/user/getAllFollower

注释：获得用户的所有关注者

method: GET

return: 

200, {'follower': user_common.all_follower(user_id=user_id)}

## GetAllFollowed

url: http://xxx/user/getAllFollowed

注释：获得所有关注该用户的user_id

method: GET

return: 

200, {'followed': user_common.all_follow(user_id=user_id)}

## GetUserInfo

url: http://xxx/user/getUserInfo/<int:user_id>>

注释：在登陆之后才能被响应, 成功返回一个用户信息的json,失败返回None 和 401

method: GET

return: 

200, {'user_info': res}

401    None

## UpdateUserInfo

注释： 更新用户信息，不包括密码，头像链接和角色。一次可以更新1-3个项目, 必须传递user_id
       
url = http://xxx/user/updateUserInfo

method = post

args:{
   
    "user_id"
    "account" 
    "name"
    "signed"   
   

}

return:

200 {user_common.get_user_info(args.get('user_id')) }

400 {'msg': 'no user_id'}

404 {'msg': 'no this user'}

403 {'msg': 'upload failure'}

## WriteBlog(可用)

url: http://xxx/blog/writeBlog

注释：进入编写blog 页面时请求这个url 获得一个上传图片的token

method: GET

return: 

200, {'token': upload_common.get_upload_token('picture')}

## FinishBlog

url: http://xxx/blog/finishBlog

注释： 图片上传完成后报告图片链接

method：POST

args:{

    "temp_id"
    "links"
}

return:

403,{'msg': '信息不全'}

200,{'msg', 'finish blog'}

404,{'msg', 'no this blog'}

403,{'msg', 'wrong pic_num'}

## LikeThisBlog (可用)

url: http://xxx/blog/likeBlog

注释：

method：POST

args:{

    "blog_id"
    "user_id"
}

return:

403,{'msg': 'must login before like blog'}

200,{'msg': 'dislike successful'}

400,{'msg': 'dislike failure'}

200,{'msg': 'like successful'}

400,{'msg': 'like failure'}


## CommentBlog

url: http://xxx/blog/commentBlog

注释：给博客添加评论

method：POST

args:{

    "blog_id"
    "author_id"
    "comment_content"
    "parent_comment_id"
    
}

return:

403,{'msg': 'must login before post blog'}

200,{'msg': '发表评论成功'}

400,{'msg': '发表评论失败'}



## BlogCache（可用）

url: http://xxx/blog/BlogCache

注释：编写完成blog, 向服务器发送文字内容，和用户信息以及待上传的图片数量

流程 客户端发送文字信息->服务端返回临时id->客户端返回图片链接

method：POST

args:{

    "user_id"
    "blog_content"
    "pic_num"
    "type"
    
}

return:

403,{'msg': 'must login before post blog'}

403,{'msg': '信息不全，发布失败'}

200,{'temp_id': temp_id}

200,{'msg': 'finish blog'}


## GetBlogByType（可用）

url: http://xxx/blog/GetBlogByType

注释：得到某个类型的博客，时间靠前的再前

method：POST

args:{

    "blog_type"
    "page_index"
    "page_count"
    "user_id"
    
}

return:

404,{'msg': 'no blog or error', 'blog_list':[]}

200,{'msg': 'no error', 'blog_list': [
{"blog_id":, 

"type": ,

"time":  ,# 格式是时间戳，使用时转换成时间，

"disablecommnet":, 是否可以评论，

 "content": blog 内容，
 
 "star_count": ,点赞数
 
 "comment_count": , 评论数
 
 "author_id": , 作者的id
 
 "author_name": ,
 
 "author_avatar_link": ,作者头像图片链接
 
 "had_star": 是否点赞过
 ]
}



## GetBlogComment

url: http://xxx/blog/GetBlogComment

注释：返回博客的全部评论，但不包括楼中楼

method：GET

return:

200，res_list

404,{'msg': 'no comment'}, statues_code

403,{'msg': 'have some error'}, statues_code


## GetUserBlog（可用）

url: http://xxx/blog/GetUserBlog

注释：

method：POST

args:{

    "user_id"
    "query_user_id"
    "page_index"
    "page_count"
    
}

return:

403,{'msg': 'must login before get user blogs'}

400,{'msg': 'must have query_user id'}

404,{'msg': 'no blog or have error', 'blog_list':[]}

200,{'msg': 'no error', 'blog_list': res_list }


## GetCommentComment

url: http://xxx/blog/GetCommentComment

注释：得到一个评论的评论，不包括楼中楼

method：GET

return:

200,res_list

404,{'msg': 'no comment'}, statues_code

403,{'msg': 'have some error'}, statues_code


## GetFollowerBlog

url: http://xxx/blog/GetFollowerBlog

注释：得到已关注的人的blog

method: POST

args:{

    "user_id"
    "page_index"
    "page_count"
   
}

return:

401,{'msg': 'need login'}

404,{'msg': 'no blog or have error', 'blog_list': []}

200,{'msg': 'no error', 'blog_list': res_list}


