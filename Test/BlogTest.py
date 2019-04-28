from requests import post, get
import json
from qiniu import Auth, put_file, etag
import qiniu.config

class BlogTest:
    def __init__(self,**kwargs):
        self.__testUser = {'account':'1234@qq.com', 'password':'123456'}
        self.user_account = kwargs.get("account",self.__testUser['account'])
        self.user_passowrd = kwargs.get("password", self.__testUser['password'])
        self.test_host = "http://39.105.64.7"
        self.local_test_host = "http://localhost:5000"

    def login(self):
        res = post("http://39.105.64.7/user/login", data={'account': self.user_account, 'password': self.user_passowrd})
        if res.status_code == 200:
            self.user_id = json.loads(res.content).get("user_id")
        else:
            print("login failuer")
            return self.login()

    # test post blog without picture
    def post_test(self):
        # send word to server
        print("send a blog without picture:")
        test_contents = ["你好" + str(index) for index in range(10)]
        for test_content in test_contents:
            res = post(self.test_host+"/blog/BlogCache", data={'user_id':self.user_id, 'blog_content':test_content, 'pic_num':0, 'type':'testing'})
            if res.status_code == 200:
                print(test_content + "post successful")
            else:
                print(json.loads(res.content)['msg'])

    def get_blog_without_picture(self):
        print("get picture without picture:")

        res = post(self.test_host+'/blog/GetUserBlog', data = {'user_id': self.user_id, 'query_user_id':self.user_id, 'page_index' : 1, 'page_count': 10})
        if res.status_code == 200:
            res = json.loads(res.content)
            ids = [info["blog_id"] for info in res['blog_list']]
            print([info['star_count'] for info in res['blog_list']])
            return ids
        else:
            print(res.content)
            return []

    def like_blog(self,blog_ids):
        for id  in blog_ids:
            res = post(url=self.test_host+"/blog/likeBlog",data={'blog_id':id,'user_id':self.user_id})
            if res.status_code == 200:
                print(json.loads(res.content)['msg'])
    
    def update_picture(self):
        token = get(self.local_test_host + '/blog/writeBlog')
        return token

if __name__ == "__main__":
    blog_test = BlogTest()
    blog_test.login()
    token = blog_test.update_picture()
    token = json.loads(token.content)['token']
    # QINIU_AK = 'n-L5hqPtAUVS6Xe9UwxFO6WIw64_O6kpQhWByXVf'
    # QINIU_SK = 'gFkEghbNYGMBSdPZ1I8EaH50pbpDRwDUCkfzqH2H'
    # q = Auth(QINIU_AK, QINIU_SK)
    # bucket_name = "blogpicture"
    picture_name = "夜と雨.jpg"
    picture_path = "E:\P站图\\"+picture_name
    # token = q.upload_token(bucket_name, None, 3600)
    res, info = put_file(token, picture_name, picture_path)
    print(res)
    print(info)