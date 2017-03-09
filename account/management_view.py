from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.conf import settings
from django.core.files import File
from django.http import Http404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import PermissionDenied

# Django Restful Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

# Authentication
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Model Related
from .models import User
from projectlog.models import UserLog
from rolepermission.models import Role, UserRole
from system.models import Menu

# Serializer
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer, ManageSerializer
#from system.serializers import MenuLoginSerializer

# Helper function
from Utils.common import paginate_data, get_client_ip, format_response, get_user_menu
from Utils.validation import password_validation_check
from Utils.send_email import send_email_with_token
from Utils.image_process import make_image_thumb

# Permissions 
from rolepermission.permissions import is_admin_or_owner, IsAdminOrReadOnly

class Login(APIView):
    """
    User login, suport username/email password combination authentication
    """
    permission_classes = ([AllowAny,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = LoginSerializer

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_class


    def post(self, request, format=None):
        context = {}
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_usable:
                    if user.is_active:
                        django_login(request, user)
                        payload = jwt_payload_handler(user)
                        token = jwt_encode_handler(payload)
                        menu = get_user_menu(user)
                        ip = get_client_ip(request)
                        UserLog.objects.create(user=user, ip=ip)
                        serializer = UserSerializer(user)
                        payload = {
                                    'token': token, 
                                    'user':serializer.data,
                                    'menu': menu
                                }
                        format_response(context, True, payload)
                        return Response(context, status=status.HTTP_200_OK)
                    else:
                        format_response(context, False, None, {'non_field_errors': '当前账户尚未激活'})
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)
                else:
                    format_response(context, False, None, {'non_field_error': '当前账户被禁用'})
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                format_response(context, False, None, {'non_field_error': '验证失败'})
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            format_response(context, False, None, {'non_field_errors':'账户密码组合出错'})
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class  Logout(APIView):
    """"
    Log the user out
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes =(JSONRenderer, BrowsableAPIRenderer,)

    def post(self, request, format=None):
        context = {}
        django_logout(request)
        format_response(context, True, None)
        return Response(context, status=status.HTTP_200_OK)

class Accounts(APIView):
    """
    Adding a system account, or get a system account list
    """
    permission_classes = ([IsAuthenticated, IsAdminOrReadOnly])
    renderer_classes =(JSONRenderer, BrowsableAPIRenderer,)
    serializer_class = UserCreateSerializer

    def get(self, request, format=None):
        context = {}
        users = User.objects.all()
        # query parameters to filter some records
        if 'is_active' in request.GET:
            active = int(request.GET['is_active'])
            users = users.filter(is_active=active)
        if 'is_usable' in request.GET:
            enable = int(request.GET['is_usable'])
            users = users.filter(is_usable=enable)
        if 'username' in request.GET:
            username = request.GET['username']
            users = users.filter(username__icontains=username)
        if 'real_name' in request.GET:
            real_name = request.GET['real_name']
            users = users.filter(real_name__icontains=real_name)
        payload = paginate_data(request, users, UserSerializer)
        format_response(context, True, payload)
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        context = {}
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            if settings.ACTIVATION:
                # Activate procedure
                base_url = '/accounts/confirmation/'
                title = 'SMonitor项目： 点击下面链接进行账户激活'
                content = '你在SMonitor注册了新的账户， 请点击下面的链接进行账户激活。'
                token, result = send_email_with_token(base_url, title, content, serializer.validated_data['email'])
                if result:
                    instance = serializer.save(confirm_code=token)
                    #serializer = UserSerializer(instance)
                    format_response(context, True, serializer.data)
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    format_response(context, False, None, {'non_field_errors': '邮件发送系统好像出了问题...'})
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(is_active=True)
                format_response(context, True, serializer.data)
                return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class Configuration(APIView):
    permission_classes = ([IsAuthenticated, IsAdminOrReadOnly])
    renderer_classes = ([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = ManageSerializer
    """
    Disable, enable, delete specific users, specified by operation 
    """
    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, format=None):
        context= {}
        serializer = ManageSerializer(data=request.data)
        if serializer.is_valid():
            data= serializer.validated_data
            operation = data['operation']
            print(data)
            users = User.objects.filter(id__in = data['user_list'])
            if operation == 'DISABLE':
                users.update(is_usable=False)
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
            elif operation == 'ENABLE':
                users.update(is_usable=True)
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
            elif operation == 'DELETE':
                users.delete()
                format_response(context, True, None)
                return Response(context, status=status.HTTP_200_OK)
        else:
            format_response(context, False, None, serializer.errors)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
