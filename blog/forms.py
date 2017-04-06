from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post, Comment, Status
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    text = forms.CharField (widget=PagedownWidget) #uklonit za normalnu
    #publish = forms.DateField (widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )
        help_texts = { #za uklanjanj poruke oko required znakova
            'username': None,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('status',)
        help_texts = { #za uklanjanj poruke oko required znakova
            'status': None,
        }
