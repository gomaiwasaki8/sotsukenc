import os
from django import forms
from django.core.mail import EmailMessage
from .models import Skillseat, Language, Course, Favorite, Request, Chat, Evaluation, Inquiry, News, Block
import datetime

class SkillseatCreateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('user_name', 'gender', 'age', 'user_img',)
    #     fields = "__all__"
    #     excludeで入力させない列を指定
    #     exclude = ("create_at")

    gender = forms.fields.ChoiceField(choices=(('男', '男'), ('女', '女'), ('その他', 'その他')), label='性別', required=True,
                                   widget=forms.widgets.RadioSelect)
    age = forms.fields.DateField(label="生年月日", widget=forms.DateInput(attrs={"type": "date", "min": "1500-04-01", "max": datetime.date.today(), "value": datetime.date.today()}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LanguageCreateForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('genre_1', 'genre_2', 'career', 'language_detail')

        # テキストエリアの高さ、幅を指定
        widgets = {
            'genre_1': forms.Textarea(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）OS", 'id': "language_0", 'name': "genre1_0"}
            ),
            'genre_2': forms.Textarea(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）Linux", 'id': "language_0", 'name': "genre2_0"}
            ),
            'career': forms.Textarea(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）x年xか月", 'id': "language_0", 'name': "career_0"}
            ),
            'language_detail': forms.Textarea(
                attrs={'rows': 1, 'cols': 30, 'placeholder': "例）環境設計・構築が可能",
                       'id': "language_0", 'name': "language_detail_0"
                       }),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'


class InquiryCreateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('user_name', 'email', 'inquiry_content',)
        # テキストエリアの高さ、幅を指定
        widgets = {
            'user_name': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
            'email': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
            'inquiry_content': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
