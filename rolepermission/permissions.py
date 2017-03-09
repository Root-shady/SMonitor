from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

# Model 
from account.models import User


# 是否为管理员，是的话则可以进行操作，否则只能进行查看
class IsAdminOrReadOnly(BasePermission):
    """
    Custome permission to only allow admin to update an object or edit it
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_admin

class IsAdmin(permissions.BasePermission):
    """Only Admin can grant permissions"""
    def has_permission(self, request, view):
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin

class IsAdminOrOwner(permissions.BasePermission):
    """Admin or Owner  otherwise, it can only be read only"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_admin:
            return True
        else:
            user = request.user
            return obj.username == user.username

def is_admin_or_owner(request, username):
    user = request.user
    if not user.is_admin:
        if user.username != username:
            raise PermissionDenied('非法操作')
    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
    return user
