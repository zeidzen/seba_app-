# Create your views here.
from django.shortcuts import render
from rest_framework.response import  Response 
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework import viewsets  
from rest_framework.permissions import IsAuthenticated ,IsAdminUser ,AllowAny 
from django.forms.models import model_to_dict
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
import jwt
from users.models import  Setting
import random
# Create your views here.


class LanguageView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


    @action(detail=True, methods=['get'],permission_classes=[IsAuthenticated])
    def levels (self, request, pk):
        token =jwt.decode (request.META['HTTP_AUTHORIZATION'].split()[1],None ,None)
        user_id = token['user_id']
        
        obj_statistics = Statistics.objects.get(user_id = user_id)
        obj_language = Language.objects.filter(id = pk)

        if obj_language.exists() : 
            levels = LanguageLevels.objects.filter(language_id = pk).values()
            levels_data = list()
            for level in levels :
                obj_course = Courses.objects.filter(
                    language_level_id = level['id'],
                    course_num = 1
                )
                if obj_course.exists(): 
                    obj_enrollment = Enrollments.objects.filter(
                        user_id = user_id,
                        course_id =obj_course[0]['id']  
                    )
                if obj_enrollment.exists(): 

                    if level['is_free'] :
                        level['status'] =True
                    else : 
                        obj_setting = Setting.objects.get(user_id =user_id )
                        if obj_setting.premium : 
                            level['status'] =True
                        else : 
                            level['status'] = False    
                else : 
                    level['status'] = False 

                serializer = LanguageLevelsSerializer(level)
                levels_data.append(serializer.data)
            return Response(levels_data)
        else : 
            return Response({"detail": "Not found."})



    
class LanguageLevelsView (viewsets.ModelViewSet):
    queryset = LanguageLevels.objects.all()
    serializer_class = LanguageLevelsSerializer


    def get_serializer_class(self) :
        if self.action =='quiz_mark' :
            return QuizMarkSerializer
        else : 
            return LanguageLevelsSerializer


class LangToLearnView(viewsets.ModelViewSet):
    queryset = LangToLearn.objects.all()
    serializer_class = LangToLearnSerializer



class whyToLearnView(viewsets.ModelViewSet):
    queryset = WhyToLearn.objects.all()
    serializer_class = WhyToLearnSerializer


class FeedbackView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    

