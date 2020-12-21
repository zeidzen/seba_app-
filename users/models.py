
from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,PermissionsMixin
from .managers import  CustomUserManager
from random import randrange
#from courses.models import Language
# Create your models here.
from django.core.files.storage import FileSystemStorage
from smart_selects.db_fields import GroupedForeignKey


class User (AbstractBaseUser , PermissionsMixin ) :
    name = models.CharField(max_length = 100)
    email = models.EmailField('email address',unique=True)
    password = models.CharField(max_length = 1200)
    birthday = models.DateField(null=True , blank= True )
    gender = models.CharField(max_length = 20 , default='Male')
    otp = models.IntegerField(default=randrange(1000, 100000,4))
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]
    objects = CustomUserManager()

    class Meta : 
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

class Setting  (models.Model) : 
    user_id = models.ForeignKey (User , on_delete = models.CASCADE , unique=  True)
    lang = models.ForeignKey( 'language.Language' , on_delete = models.DO_NOTHING)
    sound_effects = models.BooleanField(default=True)
    motivational_messages = models.BooleanField(default=True)
    speaking_exercises = models.BooleanField(default=True)
    listening_exercises = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['lang',]

    class Meta : 
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return str (self.id)

class Notification (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    msg = models.TextField()
    is_read = models.BooleanField(default = False )
    date= models.DateTimeField(auto_now_add=True)

    class Meta : 
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__ (self) :
        return '{}'.format(self.title) 




