from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("my-shelf/", views.my_shelf, name="my_shelf"),
]
