from flask_restful import Resource, reqparse
from App.Contoral import user_common, upload_common, minibolg_common, comment_common
from datetime import datetime


# 进入编写blog 页面时请求这个url 获得一个上传图片的token
class WriteBlog(Resource):
    def get(self):
        return {'token': upload_common.get_upload_token('picture')}


# 编写完成blog, 向服务器发送文字内容，和用户信息以及待上传的图片数量
# 流程 客户端发送文字信息->服务端返回临时id->客户端返回图片链接
class BlogCache(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int)
        self.parser.add_argument('blog_content', type=str)
        self.parser.add_argument('pic_num', type=int) # 图片数量
        self.parser.add_argument('type', type=str)

    def post(self):
        args = self.parser.parse_args()
        user_id = args.get('user_id', None)
        blog_content = args.get('blog_content', None)
        pic_num = args.get('pic_num')
        blog_type = args.get('type')
        timestamp = datetime.timestamp(datetime.now())

        # check_login, 未登陆不能发 有时间用装饰器重写
        if not user_common.check_login(user_id):
            return {'msg': 'must login before post blog'}, 403

        if user_id is None or blog_content is None or pic_num is None:
            print(user_id, blog_content,pic_num)
            return {'msg': '信息不全，发布失败'}, 403

        temp_id = minibolg_common.cache_blog(user_id,blog_content,pic_num,timestamp,blog_type)
        if pic_num > 0:
            return {'temp_id': temp_id}, 200
        else:
            # 没有配图
            return {'msg': 'finish blog'}, 200


#  图片上传完成后报告图片链接
class FinishBlog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('temp_id', type=str)  # blog的临时id
        self.parser.add_argument('links', type=list)

    def post(self):
        args = self.parser.parse_args()
        temp_id = args.get('temp_id')
        links = args.get('links')
        if temp_id is None or links is None:
            return {'msg': '信息不全'}, 403
        res = minibolg_common.finish_blog(temp_id, links)
        if res == 200:
            return {'msg', 'finish blog'}
        if res == 404:
            return {'msg', 'no this blog'}, 404
        if res == 403:
            return {'msg', 'wrong pic_num'}, 403


# 给博客添加评论
class CommentBlog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('blog_id', type=int)
        self.parser.add_argument('author_id', type=int)
        self.parser.add_argument('comment_content', type=str)
        self.parser.add_argument('parent_comment_id', type=int)

    def post(self):
        args = self.parser.parse_args()
        blog_id = args.get('blog_id')
        author_id = args.get('author_id')
        parent_comment_id = args.get('parent_comment_id', None)
        comment_content = args.get('comment_content')
        if not user_common.check_login(author_id):
            return {'msg': 'must login before post blog'}, 403
        res = comment_common.send_comment(blog_id, author_id, parent_comment_id,comment_content)
        if res == 200:
            return {'msg': '发表评论成功'}
        else:
            return {'msg': '发表评论失败'}, 400


class LikeThisBlog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('blog_id', type=int)
        self.parser.add_argument('user_id', type=int)

    def post(self, **kwargs):
        args = self.parser.parse_args()
        blog_id = args.get('blog_id')
        user_id = args.get('user_id')
        if not user_common.check_login(user_id):
            return {'msg': 'must login before like blog'}, 403

        if minibolg_common.had_like(blog_id,user_id):
            # 点赞过，取消点赞
            res = minibolg_common.dislike_blog(blog_id=blog_id, user_id=user_id)
            if res == 200:
                return {'msg': 'dislike successful'}, 200
            elif res == 400:
                return {'msg': 'dislike failure'}, 400
        else:
            res = minibolg_common.like_blog(blog_id, user_id)
            if res == 200:
                return {'msg': 'like successful'}, 200
            elif res == 400:
                return {'msg': 'like failure'}, 400


# 得到某个类型的博客，时间靠前的再前
class GetBlogByType(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('blog_type')
        self.parser.add_argument('page_index', type=int)
        self.parser.add_argument('page_count', type=int)
        self.parser.add_argument('user_id')

    def post(self):
        args = self.parser.parse_args()
        user_id = args.get('user_id')
        print(args)
        res_list = minibolg_common.get_mini_blog(user_id=user_id, type=args.get('blog_type'),
                                                 page_index=args.get('page_index', None),
                                                 page_count=args.get('page_count'))
        print(res_list)
        if res_list is None:
            return {'msg': 'no blog or error', 'blog_list':[]}, 404
        else:
            return {'msg': 'no error', 'blog_list': res_list}, 200


class GetUserBlog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id')
        self.parser.add_argument("query_user_id")
        self.parser.add_argument('page_index', type=int)
        self.parser.add_argument('page_count', type=int)

    def post(self):
        args = self.parser.parse_args()
        print(args['page_index'])
        user_id = args.get('user_id',1)
        if not user_common.check_login(user_id=user_id):
            return {'msg': 'must login before get user blogs'}, 403
        query_user = args.get('query_user_id')
        if query_user is None:
            return {'msg': 'must have query_user id'}, 400
        res_list = minibolg_common.get_user_blog(user_id=user_id, page_index=args.get('page_index', 1),
                                                 page_count=args.get('page_count', 10), query_user=query_user)
        if res_list is None:
            return {'msg': 'no blog or have error', 'blog_list':[]}, 404
        else:
            return {'msg': 'no error', 'blog_list': res_list }, 200


class GetBlogComment(Resource):
    # 返回博客的全部评论，但不包括楼中楼
    def get(self, blog_id):
        res_list, statues_code = comment_common.get_blog_comment(blog_id=blog_id)
        if statues_code == 200:
            return res_list
        elif statues_code == 404:
            return {'msg': 'no comment'}, statues_code
        elif statues_code == 403:
            return {'msg': 'have some error'}, statues_code


class GetCommentComment(Resource):
   # 得到一个评论的评论，不包括楼中楼
   def get(self, commment_id):
       res_list, statues_code = comment_common.get_comment_comment(commment_id)
       if statues_code == 200:
           return res_list
       elif statues_code == 404:
           return {'msg': 'no comment'}, statues_code
       elif statues_code == 403:
           return {'msg': 'have some error'}, statues_code


class GetFollowerBlog(Resource):
    # 得到已关注的人的blog
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id')
        self.parser.add_argument('page_index')
        self.parser.add_argument('page_count')

    def post(self):
        # check_login
        args = self.parser.parse_args()
        user_id = args.get('user_id')
        if not user_common.check_login(user_id) or user_id is None:
            # 未登陆
            return {'msg': 'need login'}, 401
        page_index = args.get('page_index')
        page_count = args.get('page_count')
        res_list = minibolg_common.get_follower_blog(user_id=user_id, page_index=page_index, page_count=page_count)
        if res_list is None:
            return {'msg': 'no blog or have error', 'blog_list': []}, 404
        else:
            return {'msg': 'no error', 'blog_list': res_list}, 200
