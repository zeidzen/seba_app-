from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.core.mail import send_mail

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class QuizMarkSerializer(serializers.ModelSerializer):
    mark = serializers.IntegerField(max_value=200, min_value=0)
    class Meta:
        model = Language
        fields = ['mark']

class LanguageLevelsSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    class Meta:
        model = LanguageLevels
        fields = ['id','name','level_num','image','xp','is_active','is_free','status']

class LangToLearnSerializer(serializers.ModelSerializer):
    class Meta:
        model = LangToLearn
        fields =['id','user_id','language_id']




def send_email (subject,body,email_receiver, email_sender='info@sebawayh.com') : 
    # randrange gives you an integral value    
    send_mail(subject, body , email_sender ,[email_receiver], fail_silently=False)
    return {'msg':'message sent successfully'}

class CertificateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)
    class Meta:
        model = User
        fields = ['email','file']
    def create (self , validated_data ) :

        if recipient_list is None:
            recipient_list = [self.email]

        mail = EmailMultiAlternatives(subject, message,
                                      from_email, recipient_list)

        if html_message is not None:
            mail.attach_alternative(html_message, 'text/html')

        if attachments is not None:
            for attachment in attachments:
                mail.attach(*attachment)

        mail.send()

class WhyToLearnSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyToLearn
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id','type_feedback','user_id','id_model','rate', 'desc']