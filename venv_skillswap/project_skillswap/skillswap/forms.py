import os
from django import forms
from django.core.mail import EmailMessage
from .models import Skillseat, Language, Course, Favorite, Request, Chat, Evaluation, Inquiry, News, Block


class SkillseatCreateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('user_name', 'gender', 'age', 'user_img',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LanguageCreateForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('genre_1', 'genre_2', 'career', 'language_detail')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


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
