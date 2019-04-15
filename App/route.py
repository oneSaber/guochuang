from App.Contoral.User.user import Login, Register, Logout, Echo
from App.Contoral.User.user import LoginByPhone, RegisterByPhone, ForgetPassword, GetUserInfo
from App.Contoral.User.user import UploadAvatar, Follow, GetAllFollowed, GetAllFollower, UpdateUserInfo

from App.Contoral.MiniBlog.miniblog import WriteBlog, FinishBlog, LikeThisBlog, CommentBlog, BlogCache
from App.Contoral.MiniBlog.miniblog import GetBlogByType, GetBlogComment, GetUserBlog, GetCommentComment,GetFollowerBlog


def set_route(api):
    api.add_resource(Echo, "/echo/<input_lines>")
    api.add_resource(Login, "/user/login")
    api.add_resource(Register, "/user/register")
    api.add_resource(Logout, "/user/logout")
    api.add_resource(LoginByPhone, "/user/loginPhone/<phone_number>")
    api.add_resource(RegisterByPhone, "/user/registerPhone/<phone_number>")
    api.add_resource(ForgetPassword, "/user/forgetPassword/<phone_number>")
    api.add_resource(UploadAvatar, "/user/uploadAvatar")
    api.add_resource(Follow, "/user/follow")
    api.add_resource(GetAllFollower, "/user/getAllFollower/<int:user_id>")
    api.add_resource(GetAllFollowed, "/user/getAllFollowed/<int:user_id>")
    api.add_resource(GetUserInfo, "/user/getUserInfo")
    api.add_resource(UpdateUserInfo, "/user/updateUserInfo")

    api.add_resource(WriteBlog, "/blog/writeBlog")
    api.add_resource(FinishBlog, "/blog/finishBlog")
    api.add_resource(LikeThisBlog, "/blog/likeBlog")
    api.add_resource(CommentBlog, "/blog/commentBlog")
    api.add_resource(BlogCache, "/blog/BlogCache")
    api.add_resource(GetBlogByType, "/blog/GetBlogByType")
    api.add_resource(GetBlogComment, "/blog/GetBlogComment")
    api.add_resource(GetUserBlog, "/blog/GetUserBlog")
    api.add_resource(GetCommentComment, "/blog/GetCommentComment")
    api.add_resource(GetFollowerBlog, "/blog/GetFollowerBlog")
