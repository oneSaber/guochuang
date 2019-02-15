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
        pic_num = args.get('blog_num')
        blog_type = args.get('type')
        timestamp = datetime.timestamp(datetime.now())
        if user_id is None or blog_content is None or pic_num is None:
            return {'msg': '信息不全，发布失败'}, 403
        temp_id = minibolg_common.temp_blog(user_id, blog_content, pic_num, timestamp, blog_type)
        return {'temp_id': temp_id}


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
        res = comment_common.comment(blog_id, author_id, parent_comment_id,comment_content)
        if res == 200:
            return {'msg': '发表评论成功'}
        else:
            return {'msg': '发表评论失败'}, 400


class LikeThisBlog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('blog_id', type=int)
        self.parser.add_argument('user_id', type=int)

    def get(self, **kwargs):
        args = self.parser.parse_args()
        blog_id = args.get('blog_id')
        user_id = args.get('user_id')
