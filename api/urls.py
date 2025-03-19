
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
    path('game/<int:pk>/get/', views.get_game_from_id, name='get-game-from-id'),
    path('user/<int:pk>/', views.get_user_logs, name='get-user-logs'),
    path('createlog/', views.add_log, name='add-logs'),
    path('log/<int:pk>/delete/', views.delete_logs, name='delete-logs'),
    path('log/<int:pk>/update/', views.update_logs, name='update-logs'),
    path('log/<int:user>/<int:game>/', views.get_log, name='get-a-log'),
]

