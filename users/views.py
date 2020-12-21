from django.shortcuts import render
from rest_framework.response import  Response 
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser
from rest_framework import viewsets ,status
from .serializers import *
from .models import *
from sebawayh import settings
import jwt
from django.contrib.auth.signals import user_logged_in
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.serializers import jwt_payload_handler
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication


# Create your views here.
# users/views.py
class setting_view(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    def get_permissions(self):
        permission_classes = []
        if self.action in ['create','destroy','retrieve'] :
            permission_classes = [IsAdminUser]
        elif self.action in ['list','update','partial_update'] :
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list (self,request) :
        token =jwt.decode (request.META['HTTP_AUTHORIZATION'].split()[1],None ,None)
        user_id = token['user_id']
        obj_setting= Setting.objects.filter(
            user_id=user_id).values('id','lang','sound_effects','motivational_messages',
            'speaking_exercises','listening_exercises')
        return Response(obj_setting) 

class notification_view(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class =NotificationSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == ['create','destroy', 'retrieve']:
            permission_classes = [IsAdminUser]
        elif self.action in ['list' , 'update' , 'partial_update'] :
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list (self,request) :
        token =jwt.decode (request.META['HTTP_AUTHORIZATION'].split()[1],None ,None)
        user_id = token['user_id']
        obj_notification = Notification.objects.filter(
            user_id=user_id).values('id','title','msg','is_read','date')
        return Response(obj_notification) 

class CreateUserAPIView(viewsets.ModelViewSet):
    # Allow any user (authenticated or not) to access this url 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create' , 'list'] :
            permission_classes = [IsAdminUser] 
        elif self.action in [ 'retrieve' , 'update' , 'partial_update' , 'destroy' ] :
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class CheckEmailView (viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CheckEmailSerializer
    http_method_names = ['post']

    def create (self, request, *args, **kwargs): 
        obj_user = User.objects.filter(email=request.data['email'])
        if obj_user.exists() :
            return Response({'status':True})
        else : 
            return Response({'status':False})

