from django.urls import path

from . import views


app_name = 'skillswap'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('skillseat-create/', views.AfterLoginView.as_view(), name="skillseat-create"),
    path('skillseat-confirm/', views.UserDataView.as_view(), name="skillseat-confirm"),
]
