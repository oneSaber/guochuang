from App import db
from App.Models.models import Comment, Account, MiniBlog


class Comments:

    def send_comment(self, blog_id, author_id, parent_comment_id, comment_content):
        if parent_comment_id is None or Comment.query.filter_by(comment_id=parent_comment_id).first() is None:
            parent_comment_id = 0
        new_comment = Comment(blog_id=blog_id, comment_id=author_id,
                              parent_comment_id=parent_comment_id, comment_content = comment_content)
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
