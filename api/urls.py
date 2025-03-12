
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.add_games, name='add-games'),
    path('all/', views.view_games, name='view_games'),
    path('update/<int:pk>/', views.update_games, name='update-games'),
    path('game/<int:pk>/delete/', views.delete_games, name='delete-games'),
    path('register/', views.add_users, name='register'),
    path('login/', views.login, name='login'),
]

