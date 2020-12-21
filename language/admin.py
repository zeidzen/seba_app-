from django.contrib import admin
from rest_framework.permissions import IsAuthenticated ,IsAdminUser ,AllowAny 
from .models import *
from .form import (
    LanguageLevelsForm,
    LanguageForm
)

#https://www.webforefront.com/django/adminreadrecords.html

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    form = LanguageForm
    list_display = ('id','lang','is_active','words_number','sentance_number','date')
    #list_editable = ['is_active','words_number']
    search_fields = ('id','lang')
    #actions_on_bottom = True 
    #actions_on_top = True

    #list_display_links = ['menu','name']
    #list_per_page = 5
    #exclude = ('description', )
    #actions = [change_rating]

class LanguageLevelsAdmin(admin.ModelAdmin):
    form = LanguageLevelsForm
    list_display = ('id','name','language_id' ,'level_num','xp','is_active','is_free','date')
    #list_editable = ['is_active','is_free','xp']
    search_fields = ('id','language_id__lang','level_num','name')
    readonly_fields = ['date',]
    list_filter = ("language_id",'is_active','is_free' )


class LangToLearnAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','language_id','user_type','date')
    search_fields = ('id','user_id__name','user_id__email','language_id__lang')
    list_filter = ('language_id','user_type' )


class WhyToLearnAdmin(admin.ModelAdmin):
    list_display = ('id','user_id' ,'language_id','desc','date')
    search_fields = ('id','user_id' ,'language_id','desc','date')


admin.site.register(Language , LanguageAdmin )
admin.site.register(LanguageLevels ,LanguageLevelsAdmin )
admin.site.register(LangToLearn , LangToLearnAdmin )
admin.site.register(WhyToLearn , WhyToLearnAdmin )