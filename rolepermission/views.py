from django.shortcuts import render

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

# Models
from .models import Role, RolePermission, UserRole, Permission
from account.models import User

# Serializers
from .serializers import PermissionSerializer, RoleSerializer, RoleListSerializer

# Permissions
from .permissions import IsAdminOrReadOnly

# Utilities
from Utils.common import paginate_data, format_response


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, IsAdminOrReadOnly))
def get_permission_list_or_create(request, format=None):
    context = {}
    if request.method == 'GET':
        permissions = Permission.objects.all()
        if 'disable' in request.GET:
            disable = int(request.GET['disable'])
            permissions = permissions.filter(is_usable=disable)
        if 'search' in request.GET:
            search = request.GET['search']
            name_permissions = permissions.filter(name__icontains=search)
            iden_permissions = permissions.filter(identifier__icontains=search)
            permissions = name_permissions | iden_permissions
        payload = paginate_data(request, permissions, PermissionSerializer)
        format_response(context, True, payload)
        return Response(context, status=status.HTTP_200_OK)
    else:
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            format_response(context, True, serializer.data)
            return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdminOrReadOnly))
def permission_modify(request, pk, format=None):
    context = {}
    try:
        permission = Permission.objects.get(id=pk)
    except Permission.DoesNotExist:
        format_response(context, False, None, '非法pk，请求权限不存在')
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    serializer = PermissionSerializer(permission, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        format_response(context, True, serializer.data)
        return Response(context, status=status.HTTP_200_OK)
    else:
        format_response(context, False, None, serializer.errors)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

# 删除、禁用、启用指定权限
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminOrReadOnly))
def delete_disable_enable_permission(request, format=None):
    """
    Disable, enable, delete specific permissions
    """
    context = {}
    try:
        operation = request.data['operation']
        permission_list = request.data['permission_list']
        if not isinstance(permission_list, list):
            raise Exception('permission_list 必须是系统权限id列表')
    except Exception as e:
        format_response(context, False, None, '非法参数： %s' % e)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    permissions = Permission.objects.filter(id__in = permission_list)
    if operation == 'DISABLE':
        permissions.update(is_usable=False)
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)
    elif operation == 'ENABLE':
        permissions.update(is_usable=True)
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)
    elif operation == 'DELETE':
        permissions.delete()
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)
    else:
        format_response(context, False, None, '非法操作')
        return Response(context, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, IsAdminOrReadOnly))
def get_role_list_create(request, format=None):
    """
    Get the roles from system, or create a new role, given a permission_list 
    """
    context = {}
    if request.method == 'GET':
        roles = Role.objects.all()
        if 'disable' in request.GET:
            disable = request.GET['disable']
            roles = roles.filter(is_usable=disable)
        if 'search' in request.GET:
            search = request.GET['search']
            roles = roles.filter(name__icontains=search)
        payload = paginate_data(request, roles, RoleListSerializer)
        format_response(context, True, payload)
        return Response(context, status=status.HTTP_200_OK)
    else:
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            format_response(context, True, serializer.data)
            return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated, IsAdminOrReadOnly))
def get_role_or_update(request, pk, format=None):
    """
    Get a role detail, or update a role
    """
    context = {}
    try:
        role = Role.objects.get(id=pk)
    except Role.DoesNotExist:
        format_response(context, False, None, '非法pk，不存在该角色')
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = RoleSerializer(role)
        format_response(context, True, serializer.data)
        return Response(context, status=status.HTTP_200_OK)
    else:
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            format_response(context, True, serializer.data)
            return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

# 删除、禁用、启用指定角色
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminOrReadOnly))
def delete_disable_enable_role(request, format=None):
    """
    Disable, enable, delete specific roles
    """
    context = {}
    try:
        operation = request.data['operation']
        role_list = request.data['role_list']
        if not isinstance(role_list, list):
            raise Exception('role_list 必须是系统角色id列表')
    except Exception as e:
        format_response(context, False, None, '非法参数： %s' % e)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    roles = Role.objects.filter(id__in = role_list)
    if operation == 'DISABLE':
        roles.update(is_usable=False)
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)
    elif operation == 'ENABLE':
        roles.update(is_usable=True)
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)
    elif operation == 'DELETE':
        roles.delete()
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)
    else:
        format_response(context, False, None, '非法操作')
