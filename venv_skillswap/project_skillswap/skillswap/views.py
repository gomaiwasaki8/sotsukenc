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


class IndexView(generic.TemplateView):
    template_name = "index.html"


# アカウント登録
def skillseat_input(request):
    user = request.user.id
    # 一覧表示からの遷移や、確認画面から戻るリンクを押したときはここ。
    if request.method == 'GET':
        if Skillseat.objects.filter(user_id_id=user).exists():
            return redirect('skillswap:language-input')
        # セッションに入力途中のデータがあればそれを使う。
        form = SkillseatCreateForm(request.session.get('form_data'))
    else:
        form = SkillseatCreateForm(request.POST)
        if form.is_valid():
            # 入力後の送信ボタンでここ。セッションに入力データを格納する。
            request.session['form_data'] = request.POST

            # print("request.session['form_data]は→", request.session['form_data'])
            # request.session['user_img'] = request.FILES
            # print(request.FILES['user_img'])
            # print("request.session['user_img']は→", request.session['user_img'])
            # if request.FILES['user_img'] is None:
            context = {
                'form': form,
                # 'img': '',
            }
            # else:
            #     context = {
            #         'form': form,
            #         'img': request.FILES['user_img']
            #     }
            return render(request, '../templates/skillseat_confirm.html', context)

    context = {
        'form': form,
        'img': ''
    }
    return render(request, '../templates/skillseat_input.html', context)


def user_data_confirm(request):
    """入力データの確認画面。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    session_form_data = request.session.get('form_data')
    # session_user_img = request.session.get('user_img')
    if session_form_data is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('skillswap:skillseat-input')

    context = {
        'form': SkillseatCreateForm(session_form_data),
        # 'img': session_user_img.url
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
    # print("session_form_data['user_img']は→", session_form_data['user_img'])

    if request.method == 'POST':

        object = Skillseat.objects.create(
            user_id = request.user,
            user_name=session_form_data['user_name'],
            gender=session_form_data['gender'],
            age=session_form_data['age'],
            user_img=session_form_data['user_img'],
        )
        object.save()
        return redirect('skillswap:language-input')
    else:
        # is_validに通過したデータだけセッションに格納しているので、ここ以降の処理は基本的には通らない。
        context = {
            'form': form
        }
        return render(request, '../templates/skillseat_input.html', context)


# # フォームの増減に使うグローバル変数
# FORM_NUM = 1
# FORM_VALUES = ()
#
#
# class LanguageInput(generic.FormView):
#     template_name = "language_input.html"
#     success_url = reverse_lazy("skillswap:language-input")
#     LanguageCreateFormSet = forms.formset_factory(
#         form=LanguageCreateForm,
#         extra=1,
#         max_num=100,
#         min_num=1,
#     )
#     form_class = LanguageCreateFormSet
#
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         if FORM_VALUES:
#             kwargs['data'] = FORM_VALUES
#         return kwargs
#
#
#     def post(self, request, *args, **kwargs):
#         global FORM_NUM
#         global FORM_VALUES
#         if 'btn_add' in request.POST:
#             FORM_NUM += 1
#             FORM_VALUES = request.POST.copy()
#             FORM_VALUES['form-TOTAL_FORMS'] = FORM_NUM
#         elif 'btn_del' in request.POST and FORM_NUM > 1:
#             FORM_NUM -= 1
#             FORM_VALUES = request.POST.copy()
#             FORM_VALUES['form-TOTAL_FORMS'] = FORM_NUM
#         elif 'btn_submit' in request.POST:
#             form = request.POST
#             print(request.POST)
#             if form.is_valid():
#                 # 入力後の送信ボタンでここ。セッションに入力データを格納する。
#                 request.session['form_data'] = request.POST
#                 return redirect('skillswap:language-confirm')
#             else:
#                 print("elseの場合")
#
#         return super().post(request, args, kwargs)
#

# 言語作成JS
def language_input(request):
    user = request.user.id
    # 一覧表示からの遷移や、確認画面から戻るリンクを押したときはここ。
    if request.method == 'GET':
        if Language.objects.filter(user_id_id=user).exists():
            return redirect('skillswap:course-selection')
        # セッションに入力途中のデータがあればそれを使う。
        form = LanguageCreateForm(request.session.get('form_data'))
    else:
        # print(request.POST)
        form = LanguageCreateForm(request.POST)
        if form.is_valid():
            # 入力後の送信ボタンでここ。セッションに入力データを格納する。
            request.session['form_data'] = request.POST
            return redirect('skillswap:language-confirm')

    context = {
        'form': form
    }
    # print(context)
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
        return redirect('skillswap:skillseat-browse')
    else:
        # is_validに通過したデータだけセッションに格納しているので、ここ以降の処理は基本的には通らない。
        context = {
            'form': form
        }
        return render(request, '../templates/language_input.html', context)


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
        print("self.kwargs['user_id_id']はー＞", self.kwargs['user_id_id'])
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

    def get_context_data(self, **kwargs):
        context = super(OthersProfileCourseView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(id=self.kwargs['pk']),
            'course_list': Course.objects.filter(id=self.kwargs['pk']),
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
