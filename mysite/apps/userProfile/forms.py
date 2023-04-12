from django import forms
from django.forms import models
from apps.authentication.models import User
from .models import TeachersGroup


class ChangePasswordForm(forms.Form):
    error_css_class = "is-invalid"
    oldPassword = forms.CharField(min_length=8, required=True, error_messages={'required': 'Это поле обязательно'}, widget=forms.PasswordInput(
        attrs={
            "placeholder": 'Старый пароль',
            'class': 'form-control mb-2'
        }
    ))
    newPassword = forms.CharField(min_length=8, required=True, error_messages={'required': 'Это поле обязательно'}, widget=forms.PasswordInput(
        attrs={
            "placeholder": 'Новый пароль',
            'class': 'form-control mb-2'
        }
    ))
    passwordConfirm = forms.CharField(min_length=8, required=True, error_messages={'required': 'Это поле обязательно'}, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Подтвердите пароль',
            'class': 'form-control mb-2',
        }
    ))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self, **kwargs):
        cleaned_data = super().clean()
        user = self.user
        oldPassword = self.cleaned_data.get('oldPassword')
        newPassword = self.cleaned_data.get('newPassword')
        passwordConfirm = self.cleaned_data.get('passwordConfirm')
        if oldPassword and passwordConfirm and newPassword:
            if newPassword != passwordConfirm:
                self.add_error(None, 'Пароли не совпадают')
            if not user.check_password(oldPassword):
                self.add_error('oldPassword', 'Неправильный старый пароль')
            if user.check_password(oldPassword):
                if newPassword == oldPassword:
                    self.add_error(None, 'Старый пароль совпадает с новым!')
        return cleaned_data


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = TeachersGroup
        fields = ('group',)
        widgets = {
            'group': forms.TextInput(
                attrs={
                    "placeholder": "Название группы",
                    "class": "form-control w-50 ms-2",
                    "id": "group-input"
                }
            )}
