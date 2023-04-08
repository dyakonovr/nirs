from django.urls import path
from .views import GetGroupList

urlpatterns = [
    path('groupList/<user>/', GetGroupList.as_view(), name='getGroupList'),
]
