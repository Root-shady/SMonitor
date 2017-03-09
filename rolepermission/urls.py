from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from rolepermission import views

urlpatterns = [
        #url(r'^register/$', views.Register.as_view(), name="register"),
        url('^$', views.get_permission_list_or_create, name="获取权限列表， 或新增加一个权限"),
        url(r'^(?P<pk>[0-9]+)/$', views.permission_modify, name='权限修改'),
        url(r'^configuration/$', views.delete_disable_enable_permission, name='禁用、启用、删除指定权限'),
        url(r'roles/$', views.get_role_list_create, name='获取角色列表 或新增一个角色'),
        url(r'roles/(?P<pk>[0-9]+)/$', views.get_role_or_update, name='获取角色详情 或修改角色信息'),
        url(r'roles/configuration/$', views.delete_disable_enable_role, name='删除、禁用、启用指定角色'),
        #url(r'^profiles/(?P<username>[A-Za-z0-9_]+)/email/$', views.email_modify, name='用户邮箱修改'),
        #url(r'^profiles/(?P<username>[A-Za-z0-9_]+)/password/$', views.password_modify, name='用户密码修改'),
    ]
