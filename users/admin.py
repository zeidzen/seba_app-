from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','birthday','is_verified','is_active','is_staff','is_superuser','last_login')
    search_fields = ('id','name','email')

class SettingAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','lang','sound_effects','motivational_messages','speaking_exercises','listening_exercises','premium')
    search_fields = ('id','user_id__name','user_id__email')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','title','is_read','date',)
    search_fields = ('id','user_id__name','user_id__email')

# class LangToLearnAdmin(admin.ModelAdmin):
#     list_display = ('id','user_id','language_id','user_type','date')
#     search_fields = ('id','user_id__name','user_id__email','language_id__lang')
#     list_filter = ('language_id','user_type' )



admin.site.register(User , UserAdmin )
admin.site.register(Setting ,SettingAdmin )
admin.site.register(Notification , NotificationAdmin )
# admin.site.register(LangToLearn , LangToLearnAdmin )
