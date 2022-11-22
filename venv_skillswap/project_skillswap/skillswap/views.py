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

class IndexView(generic.TemplateView):
    template_name = "index.html"


class AfterLoginView(generic.View):
    def get(self, request):
        if Language.objects.filter(user_id_id=self.request.user).exists() and Skillseat.objects.filter(user_id_id=self.request.user).exists():
            return redirect('skillswap:inquiry')
        elif Skillseat.objects.filter(user_id_id=self.request.user).exists():
            return redirect('skillswap:')
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


# 言語作成（確認画面無し）
class LanguageCreateView(generic.CreateView):
    model = Language
    template_name = "language_create(sensei).html"
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
        return redirect("skillswap:inquiry")

    def form_invalid(self, form):
        print("失敗！")
        return super().form_invalid(form)


class SkillseatUpdateView(generic.UpdateView):
    model = Skillseat
    template_name = "skillseat_update.html"
    form_class = SkillseatUpdateForm

    success_url = reverse_lazy('skillswap:skillseat-browse')


class SkillseatBrowseView(generic.ListView):
    template_name = "skillseat_browse.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):
        context = super(SkillseatBrowseView, self).get_context_data(**kwargs)
        context.update({
            'language_list': Language.objects.filter(user_id_id=self.request.user),
            'course_list': Course.objects.filter(user_id_id=self.request.user),
        })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# プロフィール文章閲覧
class ProfileTextView(generic.ListView):
    model = Skillseat
    template_name = "profile_text.html"

    def get_queryset(self):
        profile_text = Skillseat.objects.filter(user_id_id=self.request.user)
        return profile_text


class ProfileTextUpdateView(generic.UpdateView):
    model = Skillseat
    template_name = "profile_text_update.html"
    form_class = ProfileTextCreateForm
    success_url = reverse_lazy('skillswap:profile-text')


# 講座選択
class CourseSelectionView(generic.ListView):
    model = Course
    template_name = "course_selection.html"


class MyCourseView(generic.ListView):
    model = Course
    template_name = "my_course.html"

    def get_queryset(self):
        courses = Course.objects.filter(user_id_id=self.request.user).order_by('-created_at')
        return courses


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


class MyCourseUpdateView(generic.UpdateView):
    model = Course
    template_name = "my_course_update.html"
    form_class = MyCourseCreateForm
    success_url = reverse_lazy('skillswap:my-course')


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


class OthersProfileTextView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_text.html"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileTextView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(id=self.kwargs['pk']),
        })
        return context


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
        print(context)
        return context

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
