from django import forms
from django.forms import models
from apps.authentication.models import User


class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput(
        attrs={
            "placeholder": 'Старый пароль',
            'class': 'form-control mb-2'
        }
    ))
    newPassword = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput(
        attrs={
            "placeholder": 'Новый пароль',
            'class': 'form-control mb-2'
        }
    ))
    passwordConfirm = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Подтвердите пароль',
            'class': 'form-control mb-2',
        }
    ))

