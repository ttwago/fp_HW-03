from django import forms

from .models import Post, Response


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'comment',
            'category',
        ]
        labels = {
            'title': 'Заголовок',
            'comment': '',
            'category': 'Категория',
        }


class ResponseCreateForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'comment',
        ]
        labels = {
            'comment': ''
        }
