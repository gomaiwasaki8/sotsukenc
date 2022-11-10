from django.urls import path

from . import views


app_name = 'skillswap'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('skillseat-input/', views.skillseat_input, name="skillseat-input"),
    path('skillseat-confirm/', views.user_data_confirm, name="skillseat-confirm"),
    path('skillseat-create/', views.user_data_create, name="skillseat-create"),
    path('language-input/', views.language_input, name="language-input"),
    path('language-confirm/', views.language_data_confirm, name="language-confirm"),
    path('language-create/', views.language_data_create, name="language-create"),
]
