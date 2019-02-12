from qiniu import Auth
import Config


class UploadClass:
    def __init__(self):
        self.auth = Auth(access_key=Config.Config.QINIU_AK, secret_key=Config.Config.QINIU_SK)

    def get_upload_token(self, bucket):
        if bucket == 'avatar':
            token = self.auth.upload_token(Config.TestingConfig.AVATAR_BUCKET, key=None, expires=3600)
            return token
        if bucket == 'picture':
            token = self.auth.upload_token(Config.TestingConfig.PICTURE_BUCKET, key=None, expires=3600)
            return token
