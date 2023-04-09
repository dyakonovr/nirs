from django.urls import path
from . import views

urlpatterns = [
    path('top',views.top, name='top'),
    path('about',views.about, name="about"),
]