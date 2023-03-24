from django.urls import path
from . import views

urlpatterns = [
    path('dictionary',views.dict,name='dict'),
    path('dates', views.dates, name='dates'),
]