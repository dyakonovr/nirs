from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='quiz'),
    path('profile', views.profile, name='profile'),
]
