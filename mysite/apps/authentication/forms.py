from django import forms
from .models import User
from django.forms import models


class LogInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя',
                'class': 'form-control mb-2',
            },
        ),
        min_length=5,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control mb-4',
            }
        ),
        min_length=8,
        required=True
    )


class SignUpForm(models.ModelForm):
    passwordConfirm = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Подтвердите пароль',
            'class': 'form-control mb-2',
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'phoneNumber', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Имя пользователя',
                    'min_length': 5,
                    'class': 'form-control mb-2',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Пароль',
                    'min_length': 8,
                    'class': 'form-control mb-2',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email',
                    'class': 'form-control mb-2',
                }
            ),
            'phoneNumber': forms.TextInput(
                attrs={
                    'placeholder': 'Номер телефона с кодом страны',
                    'min_length': 12,
                    'class': 'form-control mb-2',
                }
            ),
        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        passwordConfirm = self.cleaned_data.get('passwordConfirm')
        if password and passwordConfirm:
            if password != passwordConfirm:
                self.add_error(None, 'Пароли не совпадают')
        return cleaned_data
