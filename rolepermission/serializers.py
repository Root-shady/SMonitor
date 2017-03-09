from rest_framework import serializers
from .models import Role, RolePermission, Permission, UserRole

class PermissionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_usable = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Permission
        fileds = ('id',  'name', 'is_usable', 'identifier', 'created')
        extra_kwargs = {"name": {"error_messages": {"required": "权限名不能为空"}}, "identifier":{"error_messages":{"required":"权限标识符不能为空", "invalid":"非法标识符格式"}}}


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fileds = ('role', 'permission')

class RoleListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_usable = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Role
        fileds = ('id', 'name', 'description', 'is_usable', 'created')

class RoleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_usable = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    permission_list = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fileds = ('id', 'name', 'description', 'is_usable', 'created', 'permission_list', 'permissions')
        extra_kwargs = {"name": {"error_messages": {"required": "角色名不能为空"}}}

    # 个性化出错信息
    def __init__(self, *args, **kwargs):
        super(RoleSerializer, self).__init__(*args, **kwargs)
        self.fields['permission_list'].error_messages['required'] = 'permission_list不能为空'


    def create(self, validated_data):
        permission_data = validated_data.pop('permission_list')
        role = Role.objects.create(**validated_data)
        permissions = Permission.objects.filter(id__in=permission_data)
        for permission in permissions:
            RolePermission.objects.create(role=role, permission=permission)
        return role

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        if 'permission_list' in validated_data:
            permission_list = validated_data['permission_list']
            # Update the permission of the role
            RolePermission.objects.filter(role=instance).delete()
            permissions = Permission.objects.filter(id__in=permission_list)
            for permission in permissions:
                RolePermission.objects.create(permission=permission, role=instance)
        return instance

    def get_permissions(self, obj):
        plist = RolePermission.objects.filter(role=obj).values_list('permission', flat=True)
        return plist
