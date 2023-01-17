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
    # スキルシートの作成
    path('skillseat-create/', views.SkillseatCreateView.as_view(), name="skillseat-create"),
    # スキルシートの更新
    path('skillseat-update/<int:pk>/', views.SkillseatUpdateView.as_view(), name="skillseat-update"),
    # 言語の作成
    path('language-create/', views.LanguageCreateView.as_view(), name="language-create"),
    # 言語の更新
    path('language-update/<int:pk>/', views.LanguageUpdateView.as_view(), name="language-update"),
    # 言語の削除
    path('language-delete/<int:pk>/', views.LanguageDeleteView.as_view(), name="language-delete"),
    # マイページのプロフィール文章閲覧
    path('my-page/profile-text/', views.ProfileTextView.as_view(), name="profile-text"),
    # マイページのプロフィール文章更新
    path('my-page/profile-text-update/<int:pk>/', views.ProfileTextUpdateView.as_view(), name="profile-text-update"),
    # マイページのスキルシート閲覧
    path('my-page/skillseat-browse/', views.SkillseatBrowseView.as_view(), name="skillseat-browse"),
    # マイページのマイ講座閲覧
    path('my-page/my-course/', views.MyCourseView.as_view(), name="my-course"),
    # マイページのマイ講座作成
    path('my-page/my-course-create/', views.MyCourseCreateView.as_view(), name="my-course-create"),
    # マイページのマイ講座更新
    path('my-page/my-course-update/<int:pk>/', views.MyCourseUpdateView.as_view(), name="my-course-update"),
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
    # 依頼申請
    path('request-application/<int:pk>/', views.RequestApplicationView.as_view(), name="request-application"),
    # 依頼申請済みの講座
    path('my-page/requested-course/', views.RequestedCourseView.as_view(), name="requested-course"),
    # 依頼のキャンセル
    path('my-page/requested-course-cancel/<int:pk>/', views.RequestedCourseCancelView.as_view(), name="requested-course-cancel"),
    # お知らせ（依頼）
    path('news/request-received/', views.RequestReceivedView.as_view(), name="request-received"),
    # 依頼の拒否
    path('news/request-received/rejection/<int:pk>/', views.RequestRejectionView.as_view(), name="request-rejection"),
    # 依頼の許可
    path('news/request-received/permission/<int:pk>/', views.RequestPermissionView.as_view(), name="request-permission"),

    # チャット
    path('chat_room/', views.ChatRoom.as_view(), name="chat_room"),
    path("search/", views.SearchUser.as_view(), name="search_user"),
    path("addfriend/<int:user_id_id>", views.addFriend, name="addfriend"),
    # path("addfriend/<str:username>", views.addFriend, name="addfriend"),
    path("chat/<str:username>", views.get_message, name="get_message"),
    path('api/messages', views.UpdateMessage.as_view()),
    path('api/messages/<int:sender>/<int:receiver>', views.UpdateMessage.as_view()),

    # レビュー
    path("review/<int:pk>", views.ReviewView.as_view(), name="review"),
    path("review/completed/", views.ReviewCompletedView.as_view(), name="review_completed"),

    # 管理者ログイン後
    path("administrator/", views.AdministratorView.as_view(), name="administrator"),
    path("administrator/user-list/", views.UserListView.as_view(), name="user-list"),
    path("administrator/user-list/suspension/<int:user_id_id>", views.SuspensionView.as_view(), name="suspension"),
    path("administrator/inquiry-list/", views.InquiryListView.as_view(), name="inquiry-list"),
]
