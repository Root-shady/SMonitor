from django.db import models

# Create your models here.
class Server(models.Model):
    """
    Create Server instance
    """
    hostname = models.CharField(max_length=50, verbose_name='主机名')
    ip = models.CharField(max_length=20, unique=True, verbose_name='IP地址')
    port = models.PositiveSmallIntegerField(default=22, verbose_name='SSH端口')
    username = models.CharField(max_length=30, default='root', verbose_name='账户名')
    password = models.CharField(max_length=60, verbose_name='密码')
    core = models.PositiveSmallIntegerField(verbose_name='主机核数')
    memory = models.PositiveSmallIntegerField(verbose_name='主机内存MB')
    storage = models.PositiveSmallIntegerField(verbose_name='主机存储')
    stype = models.CharField(max_length=30, verbose_name='服务器类型')
    os = models.CharField(max_length=30, verbose_name='系统版本')
    bandwidth = models.CharField(max_length=10, null=True, verbose_name='网络带宽')
    location = models.CharField(max_length=20, null=True, verbose_name='地理位置')
    status = models.BooleanField(default=False, verbose_name='主机状态')
    ssh_key = models.BooleanField(default=False, verbose_name='已添加public Key')
    description = models.CharField(max_length=300, null=True, verbose_name='相关备注')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name_plural = "主机"
        app_label = 'server'


    def __str__(self):
        return self.hostname
