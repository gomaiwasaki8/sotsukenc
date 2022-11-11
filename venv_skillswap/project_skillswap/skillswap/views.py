from django.shortcuts import render

# Create your views here.

from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect

# フォームの増減に利用する
import re

from .forms import InquiryCreateForm, SkillseatCreateForm, LanguageCreateForm
from .models import Skillseat, Language, Course, Favorite, Request, Chat, Evaluation, Inquiry, News, Block


class IndexView(generic.TemplateView):
    template_name = "index.html"


# class AfterLoginView(generic.FormView):
#     model = Skillseat
#     template_name = "skillseat_create.html"
#     form_class = SkillseatCreateForm
#     success_url = reverse_lazy('skillswap:skillseat-confirm')


# アカウント登録
def skillseat_input(request):
    # 一覧表示からの遷移や、確認画面から戻るリンクを押したときはここ。
    if request.method == 'GET':
        # セッションに入力途中のデータがあればそれを使う。
        form = SkillseatCreateForm(request.session.get('form_data'))
    else:
        form = SkillseatCreateForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            # 入力後の送信ボタンでここ。セッションに入力データを格納する。
            request.session['form_data'] = request.POST
            return redirect('skillswap:skillseat-confirm')

    context = {
        'form': form
    }
    return render(request, '../templates/skillseat_input.html', context)


def user_data_confirm(request):
    """入力データの確認画面。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    session_form_data = request.session.get('form_data')
    if session_form_data is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('skillswap:skillseat-input')

    context = {
        'form': SkillseatCreateForm(session_form_data)
    }
    return render(request, '../templates/skillseat_confirm.html', context)

@require_POST
def user_data_create(request):
    """ユーザーを作成する。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    # ユーザー作成後は、セッションを空にしたいのでpopメソッドで取り出す。
    session_form_data = request.session.pop('form_data', None)
    if session_form_data is None:
        # ここにはPOSTメソッドで、かつセッションに入力データがなかった場合だけ。
        # セッション切れや、不正なアクセス対策。
        return redirect('skillswap:skillseat-input')

    form = SkillseatCreateForm(session_form_data)

    if request.method == 'POST':
        object = Skillseat.objects.create(
            user_id = request.user,
            user_name=session_form_data['user_name'],
            gender=session_form_data['gender'],
            age=session_form_data['age'],
            user_img=session_form_data['user_img']
        )
        object.save()
        return redirect('skillswap:language-input')
    else:
        # is_validに通過したデータだけセッションに格納しているので、ここ以降の処理は基本的には通らない。
        context = {
            'form': form
        }
        return render(request, '../templates/skillseat_input.html', context)


# 言語作成
def language_input(request):
    # 一覧表示からの遷移や、確認画面から戻るリンクを押したときはここ。
    if request.method == 'GET':
        # セッションに入力途中のデータがあればそれを使う。
        form = LanguageCreateForm(request.session.get('form_data'))
    else:
        form = LanguageCreateForm(request.POST)
        if form.is_valid():
            # 入力後の送信ボタンでここ。セッションに入力データを格納する。
            request.session['form_data'] = request.POST
            return redirect('skillswap:language-confirm')

    context = {
        'form': form
    }
    return render(request, '../templates/language_input.html', context)


def language_data_confirm(request):
    """入力データの確認画面。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    session_form_data = request.session.get('form_data')
    if session_form_data is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('skillswap:language-input')

    context = {
        'form': LanguageCreateForm(session_form_data)
    }
    return render(request, '../templates/language_confirm.html', context)

@require_POST
def language_data_create(request):
    """ユーザーを作成する。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    # ユーザー作成後は、セッションを空にしたいのでpopメソッドで取り出す。
    session_form_data = request.session.pop('form_data', None)
    if session_form_data is None:
        # ここにはPOSTメソッドで、かつセッションに入力データがなかった場合だけ。
        # セッション切れや、不正なアクセス対策。
        return redirect('skillswap:language-input')

    form = LanguageCreateForm(session_form_data)

    if request.method == 'POST':
        object = Language.objects.create(
            user_id=request.user,
            genre_1=session_form_data['genre_1'],
            genre_2=session_form_data['genre_2'],
            career=session_form_data['career'],
            language_detail=session_form_data['language_detail']
        )
        object.save()
        return redirect('skillswap:inquiry')
    else:
        # is_validに通過したデータだけセッションに格納しているので、ここ以降の処理は基本的には通らない。
        context = {
            'form': form
        }
        return render(request, '../templates/language_input.html', context)


# class UserDataView(generic.CreateView):
#     model = Skillseat
#     template_name = "skillseat_confirm.html"
#     form_class = SkillseatCreateForm
#     # 遷移先未定のためinquiryにしてる
#     success_url = reverse_lazy('skillswap:inquiry')
#
#     def form_valid(self, form):
#         skillseat = form.save(commit=False)
#         skillseat.user_id = self.request.user
#         skillseat.save()
#         return super().form_valid(form)
#     # 失敗した時の処理特に書いてないのであとで追記するかも
#

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
