from django.urls import path, re_path
from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    re_path(r'addGroup', views.addGroup, name='addGroup')
]
