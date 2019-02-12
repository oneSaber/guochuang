from App import cache, db
from App.Models.models import Picture, MiniBlog
from Config import TestingConfig
import json
from datetime import datetime

class MiniBlog:
    def __init__(self):
        self.temp_blog = 'TEMP_BLOG'
        self.pic_namespace = TestingConfig.PICTURE_NAMESPACE

    def cache_blog(self, user_id, blog_content, pic_num, timestamp, type):
        blog_id = self.write_sql(user_id,blog_content,type)
        while blog_id == 0:
            blog_id = self.write_sql(user_id,blog_content,type)
        serialization = {'user_id': user_id,
                         'blog_content': blog_content,
                         'pic_num': pic_num,
                         'timestamp': timestamp}
        serialization_json = json.dumps(serialization)
        cache.hset(self.temp_blog, blog_id, serialization_json)
        return blog_id

    def write_sql(self,user_id, blog_content, type):
        new_blog = MiniBlog(author_id=user_id, content=blog_content, type=type,)
        try:
            db.session.add(new_blog)
            db.session.commit()
            return new_blog.my_id()
        except Exception as e:
            print(e)
            return 0

    def finish_blog(self, temp_id, links):
        temp_blog = cache.hget(self.temp_blog, temp_id)
        if temp_blog is None:
            return 404
        blog_dict = json.loads(temp_blog)
        if blog_dict['pic_num'] != len(links):
            return 403
        for link in links:
            new_pic = Picture(picture_link=self.pic_namespace+link,blog_id=temp_id)
            db.session.add(new_pic)
            db.session.commit()
        return 200
