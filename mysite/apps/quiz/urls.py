from django.urls import path
from . import views

urlpatterns = [
    path('quiz', views.index, name='quiz'),
]
