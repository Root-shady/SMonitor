from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import PermissionDenied

# Django Restful Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, renderer_classes, permission_classes, parser_classes

# Model Related
from .models import User
from rolepermission.models import Role, UserRole

# Serializer
from .serializers import UserSerializer, CodeConfirmationSerializer, PasswordResetSerializer, ProfileSerializer, EmailSerializer, PasswordModifySerializer

# Helper function
from Utils.common import paginate_data, get_client_ip, format_response, get_user_menu
from Utils.validation import password_validation_check, list_validation_check
from Utils.send_email import send_email_with_token
from Utils.image_process import make_image_thumb

# Permissions 
from rolepermission.permissions import is_admin_or_owner, IsAdminOrReadOnly

class Confirmation(APIView):
    """
    Given the query code, return the code information
    """
    permission_classes = ([AllowAny,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = CodeConfirmationSerializer

    def get_obj(self, code):
        try:
            return User.objects.get(confirm_code=code)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        context = {}
        if 'code' in request.GET:
            code = request.GET['code'].strip()
            user = self.get_obj(code)
            payload = {}
            if not user.is_active:
                payload['type'] = 1
            else:
                payload['type'] = 2
            format_response(context, True, payload)
            return Response(context, status=status.HTTP_200_OK)
        else:
            raise Http404

    def post(self, request, format=None):
        """Password Reset or Account Activiation"""
        context = {}
        serializer = CodeConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = self.get_obj(data['code'])
            # Password Reset
            if user.is_active:
                password = data['password']
                user.set_password(password)
                user.confirm_code = None
                user.save()
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
            else:
                user.is_active = True
                user.confirm_code = None
                user.save()
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class PasswordReset(APIView):
    """
    Password reset, send an reset url to the user's email, user enter username, or email
    """
    permission_classes = ([AllowAny,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = PasswordResetSerializer

    def post(self, request, format=None):
        context = {}
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                if '@' in token:
                    user = User.objects.get(emial=token)
                else:
                    user = User.objects.get(username=token)
            except User.DoesNotExist as e:
                raise Http404
            base_url = '/accounts/confirmation/'
            title = '重置密码'
            content = '点击进行相关的密码重置：'
            token, result = send_email_with_token(base_url, title, content, user.email)
            if result:
                user.confirm_code = token
                user.save()
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
            else:
                format_response(context, False, None, {'non_field_errors': '邮件发送系统好像出了问题...'})
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# 用户的相关信息编辑
# 相关的权限控制，不实现分离机制
class Profile(APIView):
    """
    Editing user profile, specific by username
    """
    permission_classes = ([IsAuthenticated,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = ProfileSerializer

    def get(self, request, username, format=None):
        context = {}
        # Permission check
        user = is_admin_or_owner(request, username)
        serializer = UserSerializer(user)
        format_response(context, True, serializer.data)
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, username, format=None):
        context = {}
        user = is_admin_or_owner(request, username)
        if request.user.is_admin:
            if 'role_list' in request.data:
                role_list = list_validation_check(request.data['role_list'])
                UserRole.objects.filter(user=user).delete()
                roles = Role.objects.filter(id__in=role_list)
                for role in roles:
                    UserRole.objects.create(user=user, role=role)
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            format_response(context, True, serializer.data)
            return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        

# 更改用户邮箱，配置是否需要重新激活账户
class EmailModify(APIView):
    """Change user account email, account reactivate may be required """
    permission_classes =  ([IsAuthenticated,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = EmailSerializer

    def put(self, request, format=None):
        context = {}
        user = is_admin_or_owner(request, username)
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                format_response(context, False, None, {'non_field_errors': '用户邮箱已被注册'})
                return Response(context, status=status.HTTP_409_CONFLICT)
            except User.DoesNotExist:
                user.email = email
                # 配置是否需要进行邮箱验证激活
                if settings.ACTIVATION:
                    # Activate procedure
                    base_url = '/accounts/confirmation/'
                    title = 'SMonitor项目邮件提醒： 账户重新激活'
                    content = '点击下面的链接重新激活账户'
                    token, result = send_email_with_token(base_url, title, content, email)
                    if result:
                        user.confirm_code = token
                        user.is_active = False
                        user.save()
                        serializer = UserSerializer(user)
                        format_response(context, True, serializer.data)
                        return Response(context, status=status.HTTP_200_OK)
                    else:
                        format_response(context, False, None, {'non_field_errors:': '邮件发送系统好像出了问题...'})
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)
                user.save()
                serializer = UserSerializer(user)
                format_response(context, True, serializer.data)
                return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class PasswordModify(APIView):
    """
    Change The Current Account Password, Provided The Original Password
    """
    permission_classes =  ([IsAuthenticated,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = PasswordModifySerializer

    def put(self, request, username, format=None):
        context = {}
        # Permission check
        user = is_admin_or_owner(request, username)
        serializer = PasswordModifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # original password check
            password = data['password']
            if user.check_password(data['origin']):
                if settings.PASSWORDCHECK:
                    if not validation_check(password):
                        format_response(context, False, None, {'non_field_errors' : '密码复杂度(至少8位，大小写字母+数字)'})
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(password)
                user.save()
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
            else:
                format_response(context, False, None, {'non_fields_errors': '旧密码错误，修改密码失败'})
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
