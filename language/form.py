from django import forms
from .models import *
from users.models import * 
from rest_framework.permissions import IsAuthenticated ,IsAdminUser ,AllowAny 
from smart_selects.db_fields import ChainedForeignKey
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.template import RequestContext



#help_text="Enter a date between now and 4 weeks (default 3)."

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'
        proxy = True
        

class LanguageLevelsForm(forms.ModelForm):
    class Meta:
        model = LanguageLevels
        fields = '__all__'
        permission_classes = [IsAuthenticated]
        
    def clean (self):
        cleaned_data = super().clean()
        level_num = self.cleaned_data.get('level_num')
        language_id = self.cleaned_data.get('language_id')
        if not level_num == 1 :
            for  index in range (1,level_num) :
                obj_language_levels =LanguageLevels.objects.filter(
                language_id =language_id,
                level_num = index )
                if  obj_language_levels.exists() : 
                        continue     
                else : 
                    raise forms.ValidationError("Please enter the Level{} first".format(index))
            return self.cleaned_data
    
        else : 
                return self.cleaned_data