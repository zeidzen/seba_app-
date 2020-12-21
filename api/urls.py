from django.urls import path , include
from rest_framework import routers
from users import  views as users_views
from authentication import  views as  authentication_views
from language import  views as languages_views

authentication_router = routers.DefaultRouter()
authentication_router.register(r'authenticating',authentication_views.authenticating_view, 'Authenticating')
authentication_router.register(r'registration',authentication_views.registration_view, 'Registration')
authentication_router.register(r'confirm_email',authentication_views.confirm_email_view, 'Confirm Email')
authentication_router.register(r'resend_code',authentication_views.resend_code_view, 'Re-send Code')
authentication_router.register(r'forgot_password',authentication_views.forgot_password_view, 'Forgot Password')
authentication_router.register(r'change_password_setting',authentication_views.change_password_setting_view, 'Change Password From Setting')
authentication_router.register(r'change_password_forgot_password',authentication_views.change_password_forgot_password_view, 'Change Password From Forgot Password')
authentication_router.register(r'user',users_views.CreateUserAPIView, 'User')
authentication_router.register(r'check_email',users_views.CheckEmailView, 'Check Email')

users_router = routers.DefaultRouter()
users_router.register(r'setting', users_views.setting_view, 'Setting')
users_router.register(r'notification', users_views.notification_view, 'Notification')

language_router = routers.DefaultRouter()
language_router.register(r'language',languages_views.LanguageView, 'Language')
language_router.register(r'language_levels', languages_views.LanguageLevelsView, 'Level Language')
language_router.register(r'lang_to_learn', languages_views.LangToLearnView, 'Language To Learn')
language_router.register(r'why_To_Learn', languages_views.whyToLearnView, 'Translate Sentence')
language_router.register(r'feedback',languages_views.FeedbackView, 'Feedback')



urlpatterns = [
    path('auth/',include(authentication_router.urls), name= 'authenticating'),
    ]
urlpatterns += users_router.urls
urlpatterns += language_router.urls


