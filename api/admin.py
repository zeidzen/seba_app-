from django.contrib import admin
from django.contrib.auth.models import Group 
from django.contrib import sites


# Register your models here.

admin.site.site_header = "Sebawayh SYSTEM ADMIN"
admin.site.site_title = "Sebawayh SYSTEM"
admin.site.index_title = "Welcome to Sebawayh API SYSTEM "
admin.site.empty_value_display = '(None)'

#admin.site.unregister(Group)
admin.site.unregister(sites.models.Site)
