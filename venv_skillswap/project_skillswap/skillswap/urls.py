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
    path('my-page/skillseat-browse/', views.SkillseatBrowseView.as_view(), name="skillseat-browse"),
    # path('my-page/my-course/', views.MyCourseView.as_view(), name="my-couse"),
    # path('my-page/favorite/', views.favoriteView.as_view(), name="favorite"),
    # path('my-page/request-course/', views.RequestCourseView.as_view(), name="request-couse"),
    # path('my-page/history-course/', views.HistoryCourseView.as_view(), name="history-course"),
]
