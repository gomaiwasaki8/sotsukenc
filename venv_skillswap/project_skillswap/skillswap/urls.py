from django.urls import path

from . import views


app_name = 'skillswap'

urlpatterns = [
    # ホーム画面
    path('', views.IndexView.as_view(), name="index"),
    # お問い合わせ
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    # ログイン後
    path('after-login/', views.AfterLoginView.as_view(), name="after-login"),
    # # スキルシートの入力
    # path('skillseat-input/', views.skillseat_input, name="skillseat-input"),
    # # スキルシートの確認
    # path('skillseat-confirm/', views.user_data_confirm, name="skillseat-confirm"),
    # # スキルシートの新規作成
    # path('skillseat-create/', views.user_data_create, name="skillseat-create"),
    # スキルシートの作成
    path('skillseat-create/', views.SkillseatCreateView.as_view(), name="skillseat-create"),
    # スキルシートの更新
    path('skillseat-update/<int:pk>/', views.SkillseatUpdateView.as_view(), name="skillseat-update"),
    # # 言語の入力
    # path('language-input/', views.language_input, name="language-input"),
    # path('language-input/', views.LanguageInput.as_view(), name="language-input"),
    # 言語の確認
    # path('language-confirm/', views.language_data_confirm, name="language-confirm"),
    # 言語の新規作成
    # path('language-create/', views.language_data_create, name="language-create"),
    # 言語の作成
    path('language-create/', views.LanguageCreateView.as_view(), name="language-create"),
    # マイページのプロフィール文章閲覧
    path('my-page/profile-text/', views.ProfileTextView.as_view(), name="profile-text"),
    # マイページのプロフィール文章更新
    path('my-page/profile-text-update/<int:pk>/', views.ProfileTextUpdateView.as_view(), name="profile-text-update"),
    # マイページのスキルシート閲覧
    path('my-page/skillseat-browse/', views.SkillseatBrowseView.as_view(), name="skillseat-browse"),
    # マイページのマイ講座閲覧
    path('my-page/my-course/', views.MyCourseView.as_view(), name="my-course"),
    # マイページのマイ講座作成
    path('my-page/my-course/create/', views.MyCourseCreateView.as_view(), name="my-course-create"),
    # マイページのマイ講座更新
    path('my-page/my-course/update/<int:pk>/', views.MyCourseUpdateView.as_view(), name="my-course-update"),
    # マイページのお気に入りの講座閲覧
    # path('my-page/favorite/', views.favoriteView.as_view(), name="favorite"),
    # マイページの依頼済みの講座閲覧
    # path('my-page/request-course/', views.RequestCourseView.as_view(), name="request-course"),
    # マイページの依頼履歴閲覧
    # path('my-page/history-course/', views.HistoryCourseView.as_view(), name="history-course"),
    # 講座選択
    path('course-selection/', views.CourseSelectionView.as_view(), name="course-selection"),
    # 講座詳細
    path('course-detail/<int:user_id_id>/', views.CourseDetailView.as_view(), name="course-detail"),
    # 相手のプロフィール（プロフィール文章）閲覧
    path('others-profile/text/<int:pk>/', views.OthersProfileTextView.as_view(), name="others-profile-text"),
    # 相手のプロフィール（講座）閲覧
    path('others-profile/course/<int:user_id_id>/', views.OthersProfileCourseView.as_view(),
         name="others-profile-course"),
    # 相手のプロフィール（スキルシート）閲覧
    path('others-profile/skillseat/<int:user_id_id>/', views.OthersProfileSkillseatView.as_view(),
         name="others-profile-skillseat"),

]
