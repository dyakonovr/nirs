from django.urls import path
from . import views

urlpatterns = [
    path('mainPage', views.mainPage, name='mainPage'),
    path('',views.aboutPage,name='about'),
]
