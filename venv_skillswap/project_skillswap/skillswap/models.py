# デフォルト
from django.db import models
# アカウントテーブルを参照するためにインポートCustomUserかAccount
from accounts.models import CustomUser


# スキルシートテーブル
class Skillseat(models.Model):

    user_id = models.OneToOneField(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    user_name = models.CharField(verbose_name='名前', max_length=30)
    gender = models.CharField(verbose_name='性別', max_length=5)
    # max_length=4
    age = models.IntegerField(verbose_name="年齢", blank=True, null=True)
    user_img = models.ImageField(verbose_name='プロフィール画像', max_length=30, blank=True, null=True)
    user_evaluation = models.FloatField(verbose_name='評価', max_length=2, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Skillseat'


# 言語テーブル
class Language(models.Model):

    user_id = models.OneToOneField(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    genre_1 = models.CharField(verbose_name="ジャンル大", max_length=100)
    genre_2 = models.CharField(verbose_name="ジャンル小", max_length=100)
    career = models.CharField(verbose_name="経歴", max_length=100, blank=True, null=True)
    language_detail = models.CharField(verbose_name="詳細", max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Language'


# 講座テーブル
class Course(models.Model):

    user_id = models.OneToOneField(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    title = models.CharField(verbose_name="講座タイトル", max_length=100)
    detail = models.CharField(verbose_name="講座詳細", max_length=500)
    course_img = models.ImageField(verbose_name='イメージ画像', max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Course'


# お気に入りテーブル
class Favorite(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    course_id = models.ForeignKey(Course, verbose_name="講座ID", on_delete=models.PROTECT, max_length=10)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Favorite'


# 依頼テーブル
class Request(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="送信者ID", on_delete=models.PROTECT, max_length=10)
    course_id = models.ForeignKey(Course, verbose_name="講座ID", on_delete=models.PROTECT, max_length=10)
    message = models.CharField(verbose_name="メッセージ", max_length=500)
    request_completed = models.BooleanField(verbose_name="依頼成立", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Request'


# チャットテーブル
class Chat(models.Model):

    request_id = models.ForeignKey(Request, verbose_name="依頼ID", on_delete=models.PROTECT, max_length=10)
    user_id = models.ForeignKey(CustomUser, verbose_name="送信者ID", on_delete=models.PROTECT, max_length=10)
    message = models.CharField(verbose_name="メッセージ", max_length=500)
    file = models.FileField(verbose_name="ファイル", max_length=500, upload_to='static/files/', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Chat'

    def __str__(self):
        return self.request_id


# 評価テーブル
class Evaluation(models.Model):

    user1_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー1ID", on_delete=models.PROTECT, max_length=10, related_name="user1_eva"
    )
    user2_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー2ID", on_delete=models.PROTECT, max_length=10, related_name="user2_eva"
    )
    # max_length=5
    evaluation_num = models.IntegerField(verbose_name="評価",)
    evaluation_text = models.CharField(verbose_name="レビュー文", max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Evaluation'


# お問い合わせテーブル
class Inquiry(models.Model):

    email = models.CharField(verbose_name="メールアドレス", max_length=256)
    user_name = models.CharField(verbose_name="名前", max_length=500)
    inquiry_content = models.CharField(verbose_name="お問い合わせ内容", max_length=500)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiry'


# お知らせテーブル
class News(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    news_detail = models.CharField(verbose_name="お知らせ内容", max_length=500)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'News'


# ブロックテーブル
class Block(models.Model):

    user1_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー1ID", on_delete=models.PROTECT, max_length=10, related_name="user1_block"
    )
    user2_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー2ID", on_delete=models.PROTECT, max_length=10, related_name="user2_block"
    )

    class Meta:
        verbose_name_plural = 'Block'
