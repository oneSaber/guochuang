from App import db, cache
from App.Models.models import Comment, Account, MiniBlog


class Comments:

    def __init__(self):
        self.child_comment_count_cache = 'CHILD_COMMENT_COUNT'
        self.blog_comment_count_cache = 'BLOG_COMMENT_cOUNT'

    def send_comment(self, blog_id, author_id, parent_comment_id, comment_content):
        # 检查parent_comment_id
        if parent_comment_id is None or Comment.query.filter_by(comment_id=parent_comment_id).first() is None:
            parent_comment_id = 0
        try:
            new_comment = Comment(blog_id=blog_id, commenter_id=author_id,
                              parent_comment_id=parent_comment_id, comment_content = comment_content)
            # 将评论数预设置为0
            cache.hset(self.child_comment_count_cache, parent_comment_id, 0)
            # 记录博客的评论数， 包括子评论
            cache.hincrby(self.blog_comment_count_cache, blog_id, 1)
            # 记录子评论数
            if parent_comment_id != 0:
                cache.hincrby(self.child_comment_count_cache, parent_comment_id, 1)

        except Exception as e1:
            print(e1)
            raise
        try:
            db.session.add(new_comment)
            db.session.commit()
            return 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return 400

    # 检查该博客是否可以评论
    def can_comment(self,blog_id):
        blog = MiniBlog.query.filter_by(blog_id=blog_id).first()
        if blog is None or blog.DisableComments is True:
            return False
        return True

    def make_response(self, comments):
        all_user = Account.query.filter(Account.id.in_([comment.commenter_id for comment in comments]))
        if all_user.count() > 0:
            res_set = [(user_info, comment) for user_info in all_user.all()
                                      for comment in comments
                                      if user_info.id == comment.commenter_id]
            res_list = []
            for res in res_set:
                user, comment = res
                res_dict = {
                    'comment_id': comment.comment_id,
                    'blog_id': comment.blog_id,
                    'comment_content': comment.comment_content,
                    'author_id': user.id,
                    'author_name': user.name,
                    'author_avatar': user.avatar_link,
                    'comment_count': cache.hget(self.child_comment_count_cache, comment.comment_id)
                }
                res_list.append(res_dict)
            return res_list
        return None

    def get_blog_comment(self, blog_id):
        # 类似虎扑，楼中楼不列出
        all_comment = Comment.query.filter(Comment.blog_id == blog_id and Comment.parent_id == 0)
        if all_comment.count() >0 :
            res_list = self.make_response(all_comment.all())
            if res_list is None:
                return None,  403
            else:
                return res_list, 200
        else:
            return None, 404

    def get_comment_comment(self, comment_id):
        all_child_comments = Comment.query.filter(Comment.parent_comment_id == comment_id)
        if all_child_comments.count() > 0:
            res_list = self.make_response(all_child_comments.all())
            if res_list is None:
                return None, 403
            else:
                return res_list, 200
        else:
            return None, 404
