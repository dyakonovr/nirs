from django.urls import path
from . import views

urlpatterns = [
    path('groupList/<int:pk>/', views.GetGroupList.as_view(), name='getGroupList'),
    path('createGroup/', views.CreateGroup.as_view(), name='getGroupList'),
    path('deleteGroup/<int:pk>/', views.DeleteGroup.as_view(), name='getGroupList'),
    path('deleteStudent/<int:pk>/',
         views.DeleteStudent.as_view(), name='deleteStudent'),
]


# Для апи:
# 1) groupList/<int:pk>/ - получение списка групп пользователя, pk - user_id.
# 2) createGroup/ - создание группы
# в body:
# user = user_id
# group = название группы
# 3) deleteGroup/<int:pk>/ - удаление группы, pk - ID ГРУППЫ!!!
# 4) deleteStudent/<int:pk>/ - удаление ученика, pk - ID ученика
