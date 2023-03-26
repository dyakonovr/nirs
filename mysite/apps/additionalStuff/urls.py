from django.urls import path
from . import views

urlpatterns = [
    path('directory',views.dict,name='dir'),
]