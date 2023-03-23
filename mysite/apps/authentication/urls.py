from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^login', views.logIn, name='login'),
    path('signUp', views.signUp, name='signUp'),
    path('logout', views.logout_view, name='logout')
]
