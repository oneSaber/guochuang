from App import cache, db
from App.Models.models import Picture, Follow,MiniBlog
from Config import TestingConfig
import json


class MiniBlogCommon:
    def __init__(self):
        self.temp_blog = 'TEMP_BLOG'
        self.pic_namespace = TestingConfig.PICTURE_NAMESPACE
        self.blog_comment_count_cache = 'BLOG_COMMENT_cOUNT'

    def star_set(self, user_id):
        return str(user_id)+'star'

    def user_cache_list(self,user_id):
        return str(user_id)+'cache_list'

    def cache_blog(self, user_id, blog_content, pic_num, timestamp, type):
        blog_id = self.write_sql(user_id,blog_content,type)
        while blog_id == 0:
            blog_id = self.write_sql(user_id,blog_content,type)
        if pic_num > 0:
            serialization = {'user_id': user_id,
                             'blog_content': blog_content,
                             'pic_num': pic_num,
                             'timestamp': timestamp}
            serialization_json = json.dumps(serialization)
            cache.hset(self.temp_blog, blog_id, serialization_json)
        return blog_id

    def write_sql(self,user_id, blog_content, type):
        new_blog = MiniBlog(author_id=user_id, content=blog_content, type=type)
        try:
            db.session.add(new_blog)
            db.session.commit()
            cache.hset(self.blog_comment_count_cache, new_blog.my_id(), 0)
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

    # 给博客点赞
    def like_blog(self, blog_id, user_id):
        try:
            if cache.hget(TestingConfig.star_cache, blog_id) is not None:
                cache.hincrby(TestingConfig.star_cache, blog_id, 1)
            else:
                cache.hset(TestingConfig.star_cache, blog_id, 1)
            # 用户id 点赞过的blog_id集合, 集合名称为str(user_id)+star
            cache.sadd(self.star_set(user_id), blog_id)
            return 200
        except Exception as e:
            print(e)
            return 400

    # 取消点赞
    def dislike_blog(self, blog_id, user_id):
        try:
            if cache.hget(TestingConfig.star_cache, blog_id) is not None and cache.sismember(self.star_set(user_id), blog_id):
                cache.hincrby(TestingConfig.star_cache, blog_id, -1)
                cache.srem(self.star_set(user_id), blog_id)
                return 200
            else:
                return 400
        except Exception as e:
            print(e)
            return 400

    def had_like(self,blog_id, user_id):
        return cache.sismember(self.star_set(user_id), blog_id)

    def like_number(self, blog_id):
        num = cache.hget(TestingConfig.star_cache, blog_id)
        if num is None:
            num = 0
        else:
            num = int(num)
        return num

    def comment_number(self, blog_id):
        num = cache.hget(self.blog_comment_count_cache, blog_id)
        if num is None:
            num = 0
        else:
            num = int(num)
        return num

    # 构建dict的response
    def make_response(self, all_blog, user_id):
        res_list = []
        for blog in all_blog:
            res_dict = {
                'blog_id': blog.blog_id,
                'type': blog.type,
                'time': blog.time.timestamp(),
                'disablecomment': blog.DisableComments,
                'content': blog.content,
                'star_count': self.like_number(blog.blog_id),
                'comment_count': self.comment_number(blog.blog_id)
            }
            # 非匿名加上用户的id
            if not blog.anonymous:
                res_dict['author_id'] = blog.author_id
                res_dict['author_name'] = blog.author.name
                res_dict['author_avatar_link'] = blog.author.avatar_link
                if res_dict['author_avatar_link'] is None:
                    res_dict['author_avatar_link'] = []
            if self.had_like(blog.blog_id, user_id):
                res_dict['had_star'] = True
            else:
                res_dict['had_star'] = False
            picture_query = Picture.query.filter(Picture.blog_id == blog.blog_id)
            if picture_query.count() != 0:
                res_dict['picture_links'] = [picture.picture_link for picture in picture_query.all()]

            res_list.append(res_dict)
        return res_list

    # def query_from_cache(self, page_count, blog_type)

    def query_from_sql(self, query_type, user_id, page_count, page,**kwargs):
        if query_type == 'blog_type':
            blog_type = kwargs.get('blog_type')
            all_blog = MiniBlog.query.filter(MiniBlog.type == blog_type)
            if all_blog.count() > (page - 1) * page_count:
                if all_blog.count() < page * page_count:
                    all_blog = all_blog.all()
                    return self.make_response(all_blog[(page- 1) * page_count:],user_id)
                else:
                    all_blog = all_blog.all()
                    return self.make_response(all_blog[(page - 1) * page_count: page_count * page - 1], user_id)
            else:
                return []

        if query_type == 'user_id':
            query_user = kwargs.get('query_user')
            all_blog = MiniBlog.query.filter(MiniBlog.author_id == query_user)
            print(all_blog.all())
            print(page, page_count)
            if all_blog.count() > (page - 1) * page_count:
                if all_blog.count() < page * page_count:
                    all_blog = all_blog.all()
                    return self.make_response(all_blog[(page - 1) * page_count:], user_id)
                else:
                    all_blog = all_blog.all()
                    return self.make_response(all_blog=all_blog[(page - 1) * page_count: page_count * page], user_id=user_id)
            else:
                return []

        if query_type == 'follower':
            # 得到关注者的新动态
            follower_list = kwargs.get('follower_list')
            all_blog = MiniBlog.query.filter(MiniBlog.author_id.in_(follower_list))
            if all_blog.count() > (page - 1) * page_count:
                if all_blog.count() < page * page_count:
                    all_blog = all_blog.all()
                    return self.make_response(all_blog[(page - 1) * page_count:], user_id)
                else:
                    all_blog = all_blog.all()
                    return self.make_response(all_blog[(page - 1) * page_count: page_count * page], user_id)
            else:
                return []

    # 按照类别来获得博客数量，按时间排序, blog_type的范围时novel, music, movie
    def get_mini_blog(self, **kwargs):
        # user_id, page_index, page_count, blog_type
        type = kwargs.get('type')
        user_id = kwargs.get('user_id')
        page_index = kwargs.get('page_index')
        if page_index is None:
            page_index = 1
        page_count = kwargs.get('page_count', 10)
        res_list = self.query_from_sql(page=page_index, page_count=page_count, query_type='blog_type', user_id=user_id, blog_type=type)
        print(res_list)
        if len(res_list) > 0 :
            return res_list
        else:
            return None

    # 得到某个用户的全部博客
    def get_user_blog(self, **kwargs):
        user_id = kwargs.get('user_id')
        page_index = kwargs.get('page_index', 1)
        page_count = kwargs.get('page_count', 10)
        query_user = kwargs.get('query_user')
        res_list = self.query_from_sql(page=page_index, page_count=page_count,query_type='user_id', user_id=user_id, query_user=query_user)
        print(res_list)
        if len(res_list) > 0:
            return res_list
        else:
            return None

    def get_follower_blog(self, **kwargs):
        user_id = kwargs.get('user_id')
        page_index = kwargs.get('page_index', 1)
        page_count = kwargs.get('page_count', 10)
        followers= all_follow = Follow.query.filter_by(follower=user_id).all()
        res_list = self.query_from_sql(page=page_index,page_count=page_count,query_type='follower',user_id=user_id, follower_list=followers)
        if len(res_list) > 0:
            return res_list
        else:
            return None
