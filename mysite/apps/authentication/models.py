from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=200, error_messages={
        'unique': 'Это имя пользователя уже занято'
    })
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=200, error_messages={
        'unique': 'Эта почта уже зарегистрирована'
    })
    phoneNumber = models.CharField(unique=True, max_length=12, error_messages={
        'unique': 'Этот номер телефона уже зарегистрирован'
    })
    first_name = None
    last_name = None
