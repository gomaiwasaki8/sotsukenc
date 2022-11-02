from django.urls import path

from . import views


app_name = 'skillswap'

urlpatterns = [
    path('', views.indexView.as_view(), name="index"),
]