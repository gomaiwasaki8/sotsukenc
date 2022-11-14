from django.urls import path

from . import views


app_name = 'skillswap'

urlpatterns = [
    # ホーム画面
    path('', views.IndexView.as_view(), name="index"),
    # お問い合わせ
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    # スキルシートの入力
    path('skillseat-input/', views.skillseat_input, name="skillseat-input"),
    # スキルシートの確認
    path('skillseat-confirm/', views.user_data_confirm, name="skillseat-confirm"),
    # スキルシートの新規作成
    path('skillseat-create/', views.user_data_create, name="skillseat-create"),
    # スキルシートの更新
    path('skillseat-update/<int:pk>/', views.SkillseatUpdate.as_view(), name="skillseat-update"),
    # 言語の入力
    path('language-input/', views.language_input, name="language-input"),
    # 言語の確認
    path('language-confirm/', views.language_data_confirm, name="language-confirm"),
    # 言語の新規作成
    path('language-create/', views.language_data_create, name="language-create"),
    # マイページのスキルシート閲覧
    path('my-page/skillseat-browse/', views.SkillseatBrowseView.as_view(), name="skillseat-browse"),
    # マイページのマイ講座閲覧
    # path('my-page/my-course/', views.MyCourseView.as_view(), name="my-couse"),
    # マイページのお気に入りの講座閲覧
    # path('my-page/favorite/', views.favoriteView.as_view(), name="favorite"),
    # マイページの依頼済みの講座閲覧
    # path('my-page/request-course/', views.RequestCourseView.as_view(), name="request-couse"),
    # マイページの依頼履歴閲覧
    # path('my-page/history-course/', views.HistoryCourseView.as_view(), name="history-course"),

]
