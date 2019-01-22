from .. import db


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
        nullable=False
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
