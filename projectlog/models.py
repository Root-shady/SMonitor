from django.db import models
from account.models import User

class UserLog(models.Model):
    user = models.ForeignKey(User, verbose_name='关联用户账号')
    ip = models.CharField(max_length=20, verbose_name='用户IP')
    created = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    class Meta:
        verbose_name_plural = '登录日志'
        app_label = 'projectlog'

    def __str__(self):
        return self.user.username

