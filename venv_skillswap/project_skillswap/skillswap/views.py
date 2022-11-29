import requests
from django.shortcuts import render

# Create your views here.

from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import *
from .models import *
from django import forms

import re


# ホーム画面（ログイン前）
class IndexView(generic.TemplateView):
    template_name = "index.html"


# ログイン後の遷移先
class AfterLoginView(generic.View):
    def get(self, request):
        if Language.objects.filter(user_id_id=self.request.user).exists() and Skillseat.objects.filter(user_id_id=self.request.user).exists():
            return redirect('skillswap:course-selection')
        elif Skillseat.objects.filter(user_id_id=self.request.user).exists():
            return redirect('skillswap:language-create')
        else:
            return redirect('skillswap:skillseat-create')


# アカウント情報新規作成（確認画面無し）
class SkillseatCreateView(generic.CreateView):
    model = Skillseat
    template_name = "skillseat_create.html"
    form_class = SkillseatCreateForm
    success_url = reverse_lazy('skillswap:language-create')

    def form_valid(self, form):
        skillseat = form.save(commit=False)
        skillseat.user_id = self.request.user
        skillseat.save()
        return super().form_valid(form)


# 言語スキルシート作成（確認画面無し。入力フォーム増減可能。）
class LanguageCreateView(generic.CreateView):
    model = Language
    template_name = "language_create.html"
    form_class = LanguageCreateForm
    success_url = reverse_lazy('skillswap:course-selection')

    def post(self, request, *args, **kwrgs):
        # 空の配列を作ります
        genre_1List = []
        genre_2List = []
        careerList = []
        language_detailList = []

        # request.POST.items()でPOSTで送られてきた全てを取得。
        for i in request.POST.items():
            # name属性のtitle_から始まるものをtitleListに追加
            if re.match(r'genres_1_*', i[0]):
                genre_1List.append(i[1])
            if re.match(r'genres_2_*', i[0]):
                genre_2List.append(i[1])
            if re.match(r'career_*', i[0]):
                careerList.append(i[1])
            if re.match(r'language_detail_*', i[0]):
                language_detailList.append(i[1])

        # titleListの要素数分を回す
        for i in range(len(genre_1List)):
            language = Language.objects.create(
                user_id_id=self.request.user.id,
                genre_1=genre_1List[i],
                genre_2=genre_2List[i],
                career=careerList[i],
                language_detail=language_detailList[i],
            )
            language.save()
        return redirect("skillswap:course-selection")

    def form_invalid(self, form):
        # print("失敗しました。")
        return super().form_invalid(form)


# アカウント情報の更新
class SkillseatUpdateView(generic.UpdateView):
    model = Skillseat
    template_name = "skillseat_update.html"
    form_class = SkillseatUpdateForm

    success_url = reverse_lazy('skillswap:skillseat-browse')


# 言語スキルシートの更新
class LanguageUpdateView(generic.UpdateView):
    model = Language
    template_name = "language_update.html"
    form_class = LanguageCreateForm

    # slug_field = "user_id_id"
    # slug_url_kwarg = "user_id_id"
    #
    # def get_context_data(self, **kwargs):
    #     context = super(LanguageUpdateView, self).get_context_data(**kwargs)
    #     context.update({
    #         'language_list': Language.objects.filter(user_id_id=self.kwargs['user_id_id']),
    #     })
    #     return context

    success_url = reverse_lazy('skillswap:skillseat-browse')


# マイページの言語スキルシート削除
class LanguageDeleteView(generic.DeleteView):
    model = Language
    template_name = "language_delete.html"

    def get_queryset(self):
        language = Language.objects.filter(id=self.kwargs['pk'])
        return language

    success_url = reverse_lazy('skillswap:skillseat-browse')


# マイページの言語スキルシート閲覧
class SkillseatBrowseView(generic.ListView):
    template_name = "skillseat_browse.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):
        context = super(SkillseatBrowseView, self).get_context_data(**kwargs)
        context.update({
            'language_list': Language.objects.filter(user_id_id=self.request.user).order_by('created_at'),
            'course_list': Course.objects.filter(user_id_id=self.request.user),
        })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# 自分のプロフィール文章閲覧
class ProfileTextView(generic.ListView):
    model = Skillseat
    template_name = "profile_text.html"

    def get_queryset(self):
        profile_text = Skillseat.objects.filter(user_id_id=self.request.user)
        return profile_text


# 自分のプロフィール文章の更新
class ProfileTextUpdateView(generic.UpdateView):
    model = Skillseat
    template_name = "profile_text_update.html"
    form_class = ProfileTextCreateForm
    success_url = reverse_lazy('skillswap:profile-text')


# 講座選択（ログイン後遷移する）
class CourseSelectionView(generic.ListView):
    model = Course
    template_name = "course_selection.html"

    def get_context_data(self, **kwargs):
        context = super(CourseSelectionView, self).get_context_data(**kwargs)
        context.update({
            'request_list': Request.objects.order_by('created_at'),
        })
        return context

    def get_queryset(self, **kwargs):
        course = super().get_queryset(**kwargs)
        query = self.request.GET

        # 検索バーから抽出
        if q := query.get('q'):
            course = course.filter(title__contains=q)
            return course.order_by('created_at')
        # 新着順
        elif query.get('new'):
            return course.order_by('-created_at')
        # 投稿順
        elif query.get('old'):
            return course.order_by('created_at')
        # それ以外
        else:
            return course.order_by('created_at')


# 自分の講座の閲覧
class MyCourseView(generic.ListView):
    model = Course
    template_name = "my_course.html"

    def get_context_data(self, **kwargs):
        context = super(MyCourseView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.request.user),
            'course_list': Course.objects.filter(user_id_id=self.request.user).order_by('-created_at')
        })
        return context


# 自分の講座作成
class MyCourseCreateView(generic.CreateView):
    model = Course
    template_name = "my_course_create.html"
    form_class = MyCourseCreateForm
    success_url = reverse_lazy('skillswap:skillseat-browse')

    def form_valid(self, form):
        course = form.save(commit=False)
        course.user_id = self.request.user
        course.save()
        return super().form_valid(form)
    # 失敗した時の処理特に書いてないのであとで追記するかも


# 自分の講座の更新
class MyCourseUpdateView(generic.UpdateView):
    model = Course
    template_name = "my_course_update.html"
    form_class = MyCourseCreateForm
    success_url = reverse_lazy('skillswap:my-course')


# 自分の講座詳細画面
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "course_detail.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"
    # pk_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
        })
        return context


# 他の人のプロフィール文章閲覧
class OthersProfileTextView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_text.html"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileTextView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(id=self.kwargs['pk']),
        })
        return context


# 他の人の講座閲覧
class OthersProfileCourseView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_course.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileCourseView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
            'course_list': Course.objects.filter(user_id_id=self.kwargs['user_id_id']),
        })
        return context


# 他の人のアカウント情報閲覧
class OthersProfileSkillseatView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_skillseat.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileSkillseatView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
            'language_list': Language.objects.filter(user_id_id=self.kwargs['user_id_id']),
        })
        return context


# 依頼申請の作成
class RequestApplicationView(generic.CreateView):
    model = Request
    template_name = "request_application.html"
    form_class = RequestApplicationCreateForm
    success_url = reverse_lazy('skillswap:course-selection')

    def form_valid(self, form):
        request = form.save(commit=False)
        request.user_id = self.request.user
        request.course_id_id = self.kwargs['pk']
        receiver = Course.objects.get(pk=self.kwargs['pk'])
        request.receiver_id_id = receiver.user_id_id
        request.save()
        return super().form_valid(form)


# 依頼申請済みの講座閲覧
class RequestedCourseView(generic.ListView):
    template_name = "requested_course.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):
        context = super(RequestedCourseView, self).get_context_data(**kwargs)
        context.update({
            'request_list': Request.objects.filter(
                user_id_id=self.request.user, request_completed__isnull=True).order_by('created_at'),
            'course_list': Course.objects.filter(request__user_id_id__exact=self.request.user).order_by('created_at'),
        })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# 依頼のキャンセル
class RequestedCourseCancelView(generic.DeleteView):
    model = Request
    template_name = "requested_course_cancel.html"
    success_url = reverse_lazy('skillswap:requested-course')


# 自分に来た依頼の閲覧
class RequestReceivedView(generic.ListView):
    model = Request
    template_name = "request_received.html"

    def get_context_data(self, **kwargs):
        context = super(RequestReceivedView, self).get_context_data(**kwargs)
        context.update({
            'request_list': Request.objects.filter(
                receiver_id_id=self.request.user, request_completed__isnull=True).order_by('created_at'),
            # 'course_list': Course.objects.filter().order_by('created_at'),
        })
        return context


# 依頼の拒否
class RequestRejectionView(generic.UpdateView):
    model = Request
    template_name = "request_rejection.html"

    def get(self, request, *args, **kwargs):
        result = Request.objects.get(pk=self.kwargs['pk'])
        result.request_completed = False
        result.save()
        return redirect('skillswap:request-received')


# 依頼の許可
class RequestPermissionView(generic.UpdateView):
    model = Request
    template_name = "request_rejection.html"

    def get(self, request, *args, **kwargs):
        result = Request.objects.get(pk=self.kwargs['pk'])
        result.request_completed = True
        result.save()
        # 後でチャット画面に遷移するコード書く
        return redirect('skillswap:request-received')




# お問い合わせ入力画面
class InquiryView(generic.CreateView):
    model = Inquiry
    template_name = "inquiry.html"
    form_class = InquiryCreateForm
    # 処理を行った後遷移する画面の指定
    success_url = reverse_lazy('skillswap:index')

    # 成功した時の処理。
    def form_valid(self, form):
        inquiry = form.save()
        inquiry.save()
        return super().form_valid(form)
    # 失敗した時の処理特に書いてないのであとで追記するかも
