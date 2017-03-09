from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Other models 
from rolepermission.models import Permission

class Menu(models.Model):
    """
    Create a system menu
    """
    title = models.CharField(max_length=30, verbose_name='菜单名称')
    url = models.CharField(max_length=100, null=True, verbose_name='关联的链接')
    pid = models.ForeignKey('self', null=True, verbose_name='菜单父节点')
    sort = models.PositiveSmallIntegerField(default=0, verbose_name='排序')
    selected = models.BooleanField(default=False, verbose_name='是否选中')

    mtype = models.PositiveSmallIntegerField(verbose_name='菜单类型')
    level = models.PositiveSmallIntegerField(default=1, verbose_name='菜单的级别')
    permission = models.ForeignKey(Permission, null=True, verbose_name='菜单对应的权限')

    is_usable = models.BooleanField(default=True, verbose_name='是否可用')
    is_visible = models.BooleanField(default=True,verbose_name='是否可见')
    created  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '菜单'
        app_label = 'system'

    def __str__(self):
        return self.title

