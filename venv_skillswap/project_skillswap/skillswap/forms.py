import os
from django import forms
from django.core.mail import EmailMessage
from .models import Skillseat, Language, Course, Favorite, Request, Chat, Evaluation, Inquiry, News, Block
import datetime


class SkillseatCreateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('user_name', 'gender', 'birthday', 'user_img', 'profile_text', )
    #     fields = "__all__"
    #     excludeで入力させない列を指定
    #     exclude = ("create_at")

    gender = forms.fields.ChoiceField(choices=(('男', '男'), ('女', '女'), ('その他', 'その他')), label='性別', required=True,)
    birthday = forms.fields.DateField(label="生年月日", widget=forms.DateInput(attrs={"type": "date", "min": "1500-04-01", "max": datetime.date.today(), "value": datetime.date.today()}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SkillseatUpdateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('user_name', 'gender', 'birthday', 'user_img', )

    gender = forms.fields.ChoiceField(choices=(('男', '男'), ('女', '女'), ('その他', 'その他')), label='性別', required=True,)
    birthday = forms.fields.DateField(label="生年月日", widget=forms.DateInput(attrs={"type": "date", "min": "1500-04-01", "max": datetime.date.today(), "value": datetime.date.today()}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileTextCreateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('profile_text',)


FIELD_NAME_MAPPING = {
        # 'Modelクラスのフィールド名' : 'name属性の値'
        'genre_1': 'genres_1_0',
        'genre_2': 'genres_2_0',
        'career': 'career_0',
        'language_detail': 'language_detail_0',
    }


class LanguageCreateForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('genre_1', 'genre_2', 'career', 'language_detail')

        # テキストエリアの高さ、幅を指定
        widgets = {
            'genre_1': forms.TextInput(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）OS", 'id': "genres_1_0", }
            ),
            'genre_2': forms.TextInput(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）Linux", 'id': "genres_2_0", }
            ),
            'career': forms.TextInput(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）x年xか月", 'id': "career_0", }
            ),
            'language_detail': forms.TextInput(
                attrs={'rows': 1, 'cols': 30, 'placeholder': "例）環境設計・構築が可能",
                       'id': "language_detail_0",
                       }),
        }

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(LanguageCreateForm, self).add_prefix(field_name)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'


# マイ講座作成フォーム
class MyCourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'detail', 'course_img',)


# 依頼申請文作成フォーム
class RequestApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('message',)


class InquiryCreateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('user_name', 'email', 'inquiry_content',)
        # テキストエリアの高さ、幅を指定
        widgets = {
            'user_name': forms.TextInput(attrs={'rows': 1, 'cols': 40}),
            'email': forms.TextInput(attrs={'rows': 1, 'cols': 40}),
            'inquiry_content': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
