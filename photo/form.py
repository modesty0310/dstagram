from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # PhotoComment model 과 연결
        fields = ['text']  # text만 받고 나머지는 서버에서 처리
