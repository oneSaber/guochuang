from .. import db
from datetime import datetime


# 用户账户表
class Account(db.Model):
    __tablename__ = "accounts"
    user_id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        index=True
    )
    account = db.Column(
        db.String(32),
        unique=True,
        nullable=False,
        index=True
        )
    password = db.Column(
        db.String(32),
        # 通过手机注册可以没有密码
    )
    name = db.Column(
        db.String(32)
    )
    # 用户角色 normal_user, vip_user, creator, admin
    role = db.Column(
        db.String(32),
        nullable=False,
        default="normal_player"
    )
    # 个人签名
    signed = db.Column(
        db.String(64),
    )
    # 头像链接
    avatar_link = db.Column(
        db.String(128),
    )

    follower = db.relationship(
        "Account", secondary="Follow", lazy="subquery",
        backref=db.backref("followed", lazy=True)
    )


# 关注表
class Follow(db.Model):
    __tablename__ = "follows"
    followed_id = db.Column(
        db.Integer,
        primary_key=True
    )
    # 关注者
    follower = db.Column(
        db.Integer,
        db.ForeignKey("accounts.user_id")
    )
    # 被关注者id
    followed = db.Column(
        db.Integer,
        db.ForeignKey("accounts.user_id")
    )


# 信息表
class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(
        db.Integer,
        primary_key=True
    )
    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.user_id")
    )
    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.user_id")
    )
    message_content = db.Column(
        db.Text
    )


# 文章内容表
class MiniBlog(db.Model):
    __tablename__ = "miniblogs"
    blog_id = db.Column(
        db.Integer,
        primary_key=True
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.user_id"),
        nullable=False
    )
    time = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    type = db.Column(
        db.String(32),
        nullable=False
    )
    author = db.relationship(
        "Account", lazy="subquery",
        backref=db.backref("blogs", lazy=True)
    )

    comment = db.relationship(
        "Comment", lazy="subquery",
        backref=db.backref("blog", lazy=True)
    )
    picture = db.relationship(
        "Picture", lazy="subquery"
    )


# 评论表
class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(
        db.Integer,
        primary_key=True
    )
    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("miniblogs.blog_id")
    )
    commenter_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.user_id")
    )
    comment_content = db.Column(
        db.Text
    )
    time = db.Column(
        db.DateTime,
        default=datetime.now
    )
    parent_comment_id = db.Column(
        db.Integer,
        nullable=True
    )
    commenter = db.relationship(
        "Account", lazy="subquery"
    )


# 图片链接表
class Picture(db.Model):
    __tablename__ = "pictures"
    picture_id = db.Column(
        db.Integer,
        primary_key=True
    )
    picture_link = db.Column(
        db.String(128),
        nullable=False
    )
    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("miniblogs.blog_id")
    )
