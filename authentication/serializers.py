
from rest_framework import serializers
from sebawayh import  settings
from django.contrib.auth.hashers import make_password , check_password
from random import randrange
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager
from users.models import *
import re
from allauth.account.adapter import get_adapter
from rest_framework import status


def send_email (subject,body,email_receiver, email_sender='info@sebawayh.com') : 
    # randrange gives you an integral value    
    send_mail(subject, body , email_sender ,[email_receiver], fail_silently=False)
    return {'msg':'message sent successfully'}



class AuthenticatingSerializer (serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        

class RegistrationSerializer (serializers.ModelSerializer):
    lang = serializers.IntegerField(min_value=0)
    class Meta (object) : 
        model = User 
        fields = ['name','birthday','email', 'password','lang','date_joined',]
        extra_kwargs = {'password': {'write_only': True} ,
                        'lang': {'min_value': 0 },
                        'date_joined':{'read_only':True},}



    def validate_name (self,value) : 
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        value = value.strip()
        error = []
        if  any(char.isdigit() for char in value)  :
            error.append("The Full Name must contain characters only")
        if not regex.search(value) == None :
            error.append("The Full Name must not contain special characters") 
        if len (value) < 3 : 
             error.append("The Full Name must length  more than 2 characters ")
        if error != [] : 
             raise serializers.ValidationError(error)
        else : 
            return value

    def validate_email(self, value):
        value = value.lower().strip()
        value = BaseUserManager.normalize_email(value)
        if User.objects.filter(email=value).exists() :
            raise serializers.ValidationError({'detail':"Email already exists."})
        return value

    def validate_password(self, value):
        
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return get_adapter().clean_password(value)
    
    def validate_lang(self, value):
        obj_language = Language.objects.filter(id=value)
        if not obj_language.exists() :
            raise serializers.ValidationError({'detail':"language is not found."})
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['otp'] = randrange(1000, 100000,4)

        obj_User = User( name = validated_data['name'],
                         email= validated_data['email'],
                         birthday = validated_data['birthday'],
                         password = validated_data['password'],
                         otp = validated_data['otp'],
                        )            
        obj_User.save()

        obj_language = Language.objects.get(id=validated_data['lang'] )

        obj_setting = Setting ( user_id = obj_User,lang =obj_language)
        obj_setting.save()

        obj_jstatistics = Statistics(
            user_id = obj_User,
            language_id =obj_language, 
        )
        obj_jstatistics.save(
            
        )
        obj_notification=Notification(user_id = obj_User,
                                      title='Welcome to the Sebawayh',
                                      msg='Welcome')
        obj_notification.save()

        # randrange gives you an integral value
        subject = 'Account verification Sebawayh app'
        body = """
        Code : {}
        """.format(validated_data['otp'])
        send_email (subject = subject, body = body , email_receiver=validated_data['email'])         
        return  validated_data 


class ConfirmEmailSerializer (serializers.Serializer):
    email = serializers.EmailField( required=True , label="email" )
    otp = serializers.CharField(max_length=6 ,required=True ) 
    class Meta(object):
        fields = ('email','otp')
        model = User

    def validate_email(self, value):
        value = value.lower().strip()
        value = BaseUserManager.normalize_email(value)
        if not User.objects.filter(email=value).exists() :
            raise serializers.ValidationError({'detail':"Email not found."})
        return value

    def create (self, validated_data):
        instance = User.objects.get(email=validated_data['email'])        
        if  str (validated_data['otp']).strip() == str (instance.otp) : 
            instance.is_verified = True
            instance.is_active = True 
            instance.save()

            obj_notification=Notification(user_id = instance,
                                        title='Account is activated',
                                        msg='Congratulations, your account has been activated successfully')
            obj_notification.save()

            return instance
        else :
            raise serializers.ValidationError({'detail':'Incorrect Code.'})



class ForgotPasswordSerializer (serializers.Serializer): 
    email = serializers.EmailField( required=True , label="email" )
    class Meta(object):
        fields = ('email')
        model = User

    def validate_email(self, value):
        value = value.lower().strip()
        value = BaseUserManager.normalize_email(value)
        if not User.objects.filter(email=value).exists() :
            raise serializers.ValidationError({'detail':"Email not found."})
        return value

    def create (self, validated_data):
        instance = User.objects.get(email=validated_data['email'])
        # randrange gives you an integral value
        instance.otp = randrange(1000, 100000,4) 
        instance.save()
        if instance.is_verified :
            subject = 'Forgot Password Sebawayh app'
        else : 
            subject = 'Account verification Sebawayh app'

        body = """
        Code : {}
        """.format(instance.otp)
        send_email (subject = subject, body = body , email_receiver=validated_data['email'])
        return instance
        


class ChangePasswordSettingSerializer (serializers.Serializer) :
    id = serializers.IntegerField() 
    old_password = serializers.CharField(required=True )
    new_password = serializers.CharField(required=True )
    confirm_password = serializers.CharField(required=True)

    class Meta (object) : 
        model = User
        fields = ('id','old_password','new_password','confirm_password')
        extra_kwargs = {'id':{'read_noly':True},
                'old_password': {'write_only': True},
                'new_password': {'write_only': True},
                'confirm_password': {'write_only': True},
                }

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError( {'detail': "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)})        
        return value

    def create (self ,validated_data ) :
        obj_user = User.objects.get(id = validated_data['id'])
        if   check_password(validated_data['old_password'] , obj_user.password ) : 

            if validated_data['new_password'] == validated_data['confirm_password'] : 
                obj_user.password = make_password (self.validate_password(validated_data['new_password']))
                obj_user.save() 

                obj_notification=Notification(user_id = obj_user,
                                        title='Password changed',
                                        msg='Your password has changed')
                obj_notification.save()

                return obj_user

            else : 
                 raise serializers.ValidationError({'detail':"password does not match."})

        else : 
            raise serializers.ValidationError({'detail':"The password is incorrect."})


class ChangeaPsswordForgotPasswordSerializer (serializers.Serializer) : 
    id = serializers.IntegerField()
    new_password = serializers.CharField(required=True )
    confirm_password = serializers.CharField(required=True)

    extra_kwargs = {'new_password': {'write_only': True},
                    'confirm_password': {'write_only': True,} ,
                    'id':{'read_noly':True}  
                    }

    class Meta (object) : 
        fields = ('id','new_password','confirm_password')
        model = User

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError( {'detail': "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)})        
        return value

    def create (self , validated_data ) : 
        obj_user = User.objects.get(id=validated_data['id'] )
        if obj_user.is_verified : 
            if validated_data['new_password'] == validated_data['confirm_password'] : 
                obj_user.password = make_password (self.validate_password(validated_data['new_password']))
                obj_user.save()
                obj_notification=Notification(user_id = obj_user,
                        title='Password changed',
                        msg='Your password has changed')
                obj_notification.save()

                return {'msg':"Password changed successfully."}
            else : 
                raise serializers.ValidationError({'detail':"password does not match."})
        else : 
            raise serializers.ValidationError({'detail':"account has not verified."})