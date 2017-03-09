from django.db import models

from account.models import User

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='角色名', error_messages={'unique':"角色名已存在"})
    description = models.CharField(max_length=100, blank=True, null=True,  verbose_name='角色的相关说明')
    is_usable = models.BooleanField(default=1, verbose_name='角色可用') 
    created = models.DateTimeField(auto_now_add=True, verbose_name='角色创建时间')

    class Meta:
        verbose_name_plural = "角色"
        app_label = 'rolepermission'


    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, verbose_name='关联员工')
    role = models.ForeignKey(Role, verbose_name='关联角色')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return user.username + " : " + role.name

    class Meta:
        verbose_name_plural = '用户角色'
        app_label = 'rolepermission'

class Permission(models.Model):
    #module = models.CharField(max_length=30, null=True,  verbose_name='权限模块')
    name = models.CharField(max_length=30, unique=True, verbose_name='权限名称', error_messages={'unique':'权限名已存在'})
    #description = models.CharField(max_length=100, null=True, verbose_name='权限的相关描述')
    identifier = models.CharField(max_length=30, unique=True, verbose_name='权限标识符', error_messages={'unique':'权限标识符已存在'})
    is_usable = models.BooleanField(default=1, verbose_name='权限可用')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name + " : " + self.identifier

    class Meta:
        verbose_name_plural = '权限'
        app_label = 'rolepermission'

class RolePermission(models.Model):
    role = models.ForeignKey(Role, verbose_name='关联的角色')
    permission = models.ForeignKey(Permission, verbose_name='关联权限')
    value = models.SmallIntegerField(default=0, verbose_name='权限状态')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name_plural = '角色权限'
        app_label = 'rolepermission'
