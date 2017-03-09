from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from account import  profile_view, management_view

urlpatterns = [
        #url(r'^register/$', views.Register.as_view(), name="register"),
        url('^$', management_view.Accounts.as_view(), name="获取账户列表，或新增加一个账户"),
        url(r'^login/$', management_view.Login.as_view(), name="login"),
        url(r'^logout/$', management_view.Logout.as_view(), name="logout"),
        url(r'^configuration/$', management_view.Configuration.as_view(), name="指定账户禁用、启用、删除"),

        url(r'^password/email/$', profile_view.PasswordReset.as_view(), name="密码重置请求"),
        url(r'^confirmation/$', profile_view.Confirmation.as_view(), name="密码重置 账户激活 Token类型查询"),

        url(r'^profiles/(?P<username>[A-Za-z0-9_]+)/$', profile_view.Profile.as_view(), name='用户资料管理, 详情获取'),
        url(r'^profiles/(?P<username>[A-Za-z0-9_]+)/email/$', profile_view.EmailModify.as_view(), name='用户邮箱修改'),
        url(r'^profiles/(?P<username>[A-Za-z0-9_]+)/password/$', profile_view.PasswordModify.as_view(), name='用户密码修改'),
    ]
