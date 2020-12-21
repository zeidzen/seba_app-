# users/serializers.py
from rest_framework import serializers
from.models import *
from sebawayh import  settings
from django.contrib.auth.hashers import make_password , check_password
from random import randrange
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['lang','sound_effects','motivational_messages','speaking_exercises',
                'listening_exercises']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields =['title','msg','is_read','date']

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    class Meta(object):
        model = User
        fields = ('id', 'email', 'name', 'birthday','date_joined','is_verified')
        extra_kwargs = {'password': {'write_only': True}}

class CheckEmailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('email',)


