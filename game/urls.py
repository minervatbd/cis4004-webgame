from django.urls import path
from game import views

urlpatterns = [
    path("", views.main, name="main"),
]