from django.shortcuts import render

# Create your views here.

from django.views import generic
from django.urls import reverse_lazy

from .forms import InquiryCreateForm
from .models import Inquiry


class IndexView(generic.TemplateView):
    template_name = "index.html"


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
