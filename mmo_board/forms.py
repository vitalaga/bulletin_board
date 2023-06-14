from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Response, User


class PostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Your title',
                'class': 'form-text',
            }),
            'content': forms.CharField(widget=CKEditorWidget())
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Login',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Your login',
                'class': 'form-text',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Your first name',
                'class': 'form-text',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Your last name',
                'class': 'form-text',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your e-mail',
                'class': 'form-text',
            })
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {
            'text': '',
        }
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Your response',
                'class': 'form-reply',
            }),
        }


class ResponseAcceptForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['approved']
        labels = {
            'approved': 'Accept response'
        }