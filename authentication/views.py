from django.shortcuts import render
from rest_framework.response import  Response 
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser
from rest_framework import viewsets ,status
from .serializers import *
from users.models import *
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


class authenticating_view (viewsets.ModelViewSet) : 
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = AuthenticatingSerializer
    http_method_names = ['post', 'head']
    def create (self , request):
        try:
            email = request.data['email'].lower().strip()
            try : 
                user = User.objects.get(email=email)
            except : 
                res = { 'detail': 'email not found' }
                return Response(res  , status=status.HTTP_400_BAD_REQUEST )
            
            password_check = check_password(request.data['password'] ,user.password )
            if not  password_check : 
                res = {'detail': 'password is not correct' }
                return Response(res , status=status.HTTP_400_BAD_REQUEST )
  
            if user.is_verified:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)

                    obj_setting = Setting.objects.get(user_id=user)
                    user_details = {'user_id':user.id ,
                                    'name' : user.name,
                                    'lang':str(obj_setting.lang),
                                    }
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details)
                except Exception as e:
                    raise e
            else:
                res = {
                    'detail': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res , status=status.HTTP_400_BAD_REQUEST )
        except KeyError:
            res = {'detail': 'please provide a email and a password'}
            return Response(res , status=status.HTTP_400_BAD_REQUEST )


class registration_view ( viewsets.ModelViewSet): 
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post','head']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            email = request.data['email'].lower().strip()
            user = User.objects.get(email=email)

            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)

            obj_setting = Setting.objects.get(user_id=user)
            user_details = {'user_id':user.id ,
                            'name' : user.name,
                            'lang':str(obj_setting.lang),
                             }
            user_details['token'] = token
            user_logged_in.send(sender=user.__class__,request=request, user=user)
            return Response(user_details)
        except KeyError:
            res = {'detail': 'error in the data entry process'}
            return Response(res , status=status.HTTP_400_BAD_REQUEST )



class confirm_email_view (viewsets.ModelViewSet): 
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = ConfirmEmailSerializer
    http_method_names = ['post','head']

    def create (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = request.data['email'].lower().strip()
        user = User.objects.get(email=email)
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        obj_setting = Setting.objects.get(user_id=user)                        
        user_details = {'user_id':user.id ,
                        'name' : user.name,
                        'lang':str(obj_setting.lang),
                        }
        user_details['token'] = token
        user_logged_in.send(sender=user.__class__,request=request, user=user)
        return Response(user_details)




class resend_code_view (viewsets.ModelViewSet): 
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer
    http_method_names = ['post','head']

    def create (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'code sent successfully'})
    


class forgot_password_view (viewsets.ModelViewSet): 
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer
    http_method_names = ['post','head']

    def create (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'code sent successfully'})
    

class change_password_setting_view (viewsets.ModelViewSet) :
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangePasswordSettingSerializer
    http_method_names = ['post','head']

    def create (self, request, *args, **kwargs): 
        token =jwt.decode (request.META['HTTP_AUTHORIZATION'].split()[1],None ,None)
        data = request.data
        data['id'] = token['user_id'] 
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':"Password changed successfully."})


class change_password_forgot_password_view (viewsets.ModelViewSet) :
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangeaPsswordForgotPasswordSerializer
    http_method_names = ['post','head']

    def create (self,request) : 
        token =jwt.decode (request.META['HTTP_AUTHORIZATION'].split()[1],None ,None)
        data = request.data
        data['id'] = token['user_id'] 
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':"Password changed successfully."})





