from django.shortcuts import render

# Create your views here.

from django.views import generic
from django.urls import reverse_lazy

from .forms import InquiryCreateForm, SkillseatCreateForm
from .models import Skillseat, Language, Course, Favorite, Request, Chat, Evaluation, Inquiry, News, Block


class IndexView(generic.TemplateView):
    template_name = "index.html"


class AfterLoginView(generic.FormView):
    model = Skillseat
    template_name = "skillseat_create.html"
    form_class = SkillseatCreateForm
    success_url = reverse_lazy('skillswap:confirm')


class UserDataView(generic.CreateView):
    model = Skillseat
    template_name = "skillseat_confirm.html"
    form_class = SkillseatCreateForm
    # 遷移先未定のためinquiryにしてる
    success_url = reverse_lazy('skillswap:inquiry')

    def form_valid(self, form):
        skillseat = form.save(commit=False)
        skillseat.user_id = self.request.user
        skillseat.save()
        return super().form_valid(form)
    # 失敗した時の処理特に書いてないのであとで追記するかも


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
