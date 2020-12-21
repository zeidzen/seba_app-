from django.db import models
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import AllowAny
from users.models import  User  
# Create your models here.
from django.core.files.storage import FileSystemStorage
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from  datetime import  datetime 

# Create your models here.

class Language  (models.Model) : 
    lang = models.CharField(max_length=50 , unique= True ,verbose_name='Language')
    flag = models.CharField( max_length = 1000, null =True ,blank= True ,verbose_name='Flag')
    desc = models.TextField(default='' , null=True, blank=True)
    words_number = models.IntegerField(default=0,null=True,blank=True)
    sentance_number =  models.IntegerField(default=0,null=True,blank=True)
    is_active = models.BooleanField(verbose_name='Activate', default=True)
    date = models.DateTimeField(auto_now_add=True ,verbose_name='Date Time' )

    class Meta : 
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.lang


language_levels_num = [ 
    (1,'Level 1'),(2,'Level 2'),(3,'Level 3'),(4,'Level 4'),(5,'Level 5'),
    (6,'Level 6'),(7,'Level 7'),(8,'Level 8'),(9,'Level 9'),(10,'Level 10'),
    ]
language_levels_num = sorted(language_levels_num)
  
class LanguageLevels (models.Model) :
    language_id = models.ForeignKey(Language, on_delete = models.CASCADE)
    name = models.CharField(max_length=100,default =None , verbose_name = 'Name' )
    level_num = models.IntegerField(choices = language_levels_num , verbose_name = 'Level Number' ) 
    image = models.CharField( max_length = 1000, null =True ,blank= True)
    xp = models.IntegerField(verbose_name='XP Points' , default=0 ,validators=[MinValueValidator(0)])
    is_active = models.BooleanField(verbose_name='Activate', default=True)
    is_free =models.BooleanField(default=True, verbose_name='Is Free')
    date = models.DateTimeField(auto_now_add=True ,verbose_name='Date Time')

    class Meta : 
        verbose_name = 'Language Level'
        verbose_name_plural = 'Languages Levels'
        unique_together = ('language_id', 'level_num')

    def __str__ (self) : 
        return  self.name

user_types = [('user','user') , ('admin','admin')]
class LangToLearn (models.Model) : 
    user_id = models.ForeignKey (User , on_delete = models.CASCADE )
    language_id = models.ForeignKey (Language ,on_delete = models.DO_NOTHING )
    user_type = models.CharField(max_length=10,default= 'user' , choices = user_types )
    date = models.DateTimeField(auto_now_add=True )

    class Meta : 
        verbose_name = 'Language To Learn'
        verbose_name_plural = 'Languages To Learn'
        unique_together = ('user_id', 'language_id','user_type')
    def __str__ (self) :
        return str (self.id)


class WhyToLearn (models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='User')
    language_id = models.ForeignKey(Language , on_delete=models.CASCADE ,verbose_name='Language' )
    desc = models.TextField( max_length = 2000)
    date = models.DateTimeField(auto_now_add=True , verbose_name='Date Time' )

    class Meta : 
        verbose_name = 'Why To Learn'
        verbose_name_plural = 'Why To Learn'

type_model = (
    ('language','language'),
    ('language_level','language_level'),
    ('course','course'),
    ('lesson','lesson'),
    ('question','question'),
)
class Feedback(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='User')
    type_feedback = models.CharField(max_length=100 ,choices = type_model , default=None)
    id_model = models.IntegerField(validators=[MinValueValidator(1)])
    desc = models.TextField( max_length = 2000 , null=True , blank=True)
    rate = models.IntegerField(validators=[MaxValueValidator(0), MinValueValidator(5)], null=True , blank=True)
    date = models.DateTimeField(auto_now_add=True , verbose_name='Date Time' )

    class Meta : 
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'


