from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied

# Django Restful Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

#Utils
from Utils.common import paginate_data, get_client_ip, format_response

# Model Related
from .models import Server

# Create your views here.
class ServerList(APIView):
    """Create a server or list all servers"""
    permission_classes = ([IsAuthenticated,])
    renderer_classes =([JSONRenderer, BrowsableAPIRenderer,])
    serializer_class = ServerCreateSerializer

    def get(self, request, format=None):
        context = {}
        servers = Server.objects.all()
        # Some filter parameter
        payload = paginate_data(request, servers, ServerSerializer)
        format_response(context, True, payload)
        return Response(context, status=status.HTTP_200_OK)




