from django.urls import path
from . import views

urlpatterns = [
    path('userscoreview/<int:pk>/', views.UserScoreView.as_view()),
    path('userscore/<int:pk>/', views.UserScoreUpdate.as_view()),
    path('userdata/<username>/', views.UserDataView.as_view()),
    path('userdata', views.UserDataList.as_view()),
    path('token/<user_id>/', views.UserTokenView.as_view()),
]


# 1) userdata/<username>/ - получение id
# 2) userdata - получение данных всез юзеров
# 3) userscoreview/<int:pk>/ - получение результатов юзера, pk = user_id
# 4) token/<user_id>/ - получение токена юзера, user_id = user_id
# 5) userscore/<int:pk>/ - обновление результатов юзера, pk = user_id, body = {
#     'user':pk,
#     'user_score_{difficulty}': user_score,
# },
# headers ={
#     'Authentication': 'Token {token}',
# }
