from rest_framework import serializers

# Models
from .models import Server

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

class ServerCreateSerializer(serializers.ModelSerializer):

