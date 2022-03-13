from calendar import c
from dataclasses import fields
from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("__all__")


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows':2,
        'cols':46
    }))
    class Meta:
        model = Comment
        fields = ("content", )