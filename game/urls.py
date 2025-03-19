from django.urls import path
from game import views

urlpatterns = [
    path("", views.main, name="main"),
    path("games", views.games, name="games"),
    path("register", views.register, name="register"),
    path("collection", views.collection, name="collection"),
]