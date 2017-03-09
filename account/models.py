from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Overwrite the CreateUser method
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('用户邮件不能为空')
        if not username:
            raise ValueError('用户名不能为空')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, password=password, is_active=True, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, password, username, **extra_fields):
        return self._create_user(email, username, password, is_admin=True, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

class User(AbstractBaseUser):
    """
    Custom user class
    """
    username = models.CharField(max_length=30, unique=True, verbose_name='用户名', error_messages={'unique':"用户名已被注册"})
    email = models.EmailField(unique=True, verbose_name='邮件', error_messages={'unique':"邮箱已经注册"})
    real_name = models.CharField(max_length=30, null=True, verbose_name='真实姓名')
    description = models.CharField(max_length=30, null=True,  verbose_name='相关描述')
    phone = models.CharField(max_length=15, null=True, verbose_name='电话号码')
    is_active = models.BooleanField(default=False, verbose_name='账户激活')
    is_usable = models.BooleanField(default=True, verbose_name='账户可用')
    is_admin = models.BooleanField(default=False, verbose_name='超级管理员')
    confirm_code = models.CharField(null=True, max_length= 40, verbose_name='相关逻辑验证码')
    photo = models.ImageField(upload_to='account/photoes/%Y/%D', null=True, verbose_name='用户头像')
    created = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name_plural = '系统用户名'
        app_label = 'account'
        ordering = ['id',]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        self.username = self.username.strip()
        super(User, self).save(*args, **kwargs)

@receiver(post_delete, sender=User)
def photo_delete_handler(sender, **kwargs):
    user = kwargs['instance']
    if user.photo:
        storage, path = user.photo.storage, user.photo.path
        storage.delete(path)
