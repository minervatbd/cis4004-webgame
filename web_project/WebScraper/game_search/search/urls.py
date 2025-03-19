from django.urls import path
from .views import home, search_game

urlpatterns = [
    path("", home, name="home"),
    path("search_game/", search_game, name="search_game"),
]
