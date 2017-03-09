import json
from django.conf import settings
from rest_framework import serializers

# Models
from .models import User
from rolepermission.models import UserRole, Role

# Helper function
from Utils.validation import password_validation_check, list_validation_check

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'real_name', 'description', 'phone', 'is_active', 'photo', 'is_usable', 'is_admin', 'roles' ,'created')

    def get_roles(self, obj):
        #id_list = UserRole.objects.filter(user=obj).values_list('role', flat=True)
        #rlist = Role.objects.filter(id__in=id_list).values_list('name')
        rlist = UserRole.objects.filter(user=obj).values_list('role__name', flat=True)
        return rlist

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
            style={'input_type': 'password'}, label='密码')
    role_list = serializers.CharField(max_length=200, write_only=True, label='角色列表')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'real_name', 'description', 'phone', 'password', 'photo', 'role_list')

    def __init__(self, *args, **kwargs):
        super(UserCreateSerializer, self).__init__(*args, **kwargs)

    def validate_password(self, value):
        """
        Check that password is strong enought for the system
        """
        if settings.PASSWORDCHECK:
            if not password_validation_check(value):
                raise serializers.ValidationError("密码复杂度(至少8位，大小写字母+数字)") 
        return value

    def validate_username(self, value):
        """
        Check @ character not showing in the username, authentication insurrance
        """
        if '@' in value:
            raise serializers.ValidationError("用户名不能出现特殊字符@") 
        return value

    def validate_role_list(self, value):
        return list_validation_check(value)

    def create(self, validated_data):
        role_data = validated_data.pop('role_list')
        user = User.objects.create(**validated_data)
        try:
            roles = Role.objects.filter(id__in=role_data)
            for role in roles:
                UserRole.objects.create(user=user, role=role)
        except Exception as e:
            print(e)
        return user


class LoginSerializer(serializers.Serializer):
    username =  serializers.CharField(required=True, max_length=100, label='用户名/邮箱')
    password = serializers.CharField(required=True, max_length=50,
                style={'input_type': 'password'}, label='密码')

class ManageSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=['DISABLE', 'ENABLE', 'DELETE'], required=True, label='操作')
    user_list = serializers.CharField(max_length=200, required=True, label='账户列表')

    def validate_user_list(self, value):
        return list_validation_check(value)

class CodeConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=60, required=True, label='凭证')
    password = serializers.CharField(write_only=True, required=False,
            style={'input_type': 'password'}, label='密码')

    def validate_password(self, value):
        if settings.PASSWORDCHECK:
            if not password_validation_check(value):
                raise serializers.ValidationError("密码复杂度(至少8位，大小写字母+数字)") 
        return value

class PasswordResetSerializer(serializers.Serializer):
    token =  serializers.CharField(required=True, max_length=100, label='用户名/邮箱')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'real_name', 'description', 'phone', 'photo')

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, min_length=None, allow_blank=False)

class PasswordModifySerializer(serializers.Serializer):
    origin = serializers.CharField(write_only=True, required=True,
            style={'input_type': 'password'}, label='原密码')
    password = serializers.CharField(write_only=True, required=True,
            style={'input_type': 'password'}, label='新密码')



