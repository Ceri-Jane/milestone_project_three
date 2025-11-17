from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # User shelf
    path("my-shelf/", views.my_shelf, name="my_shelf"),

    # Add movie
    path("add/", views.add_to_shelf, name="add_to_shelf"),

    # Change status
    path("change-status/<int:movie_id>/<str:new_status>/", 
         views.change_status, 
         name="change_status"),

    # Remove movie
    path("remove/<int:movie_id>/", 
         views.remove_movie, 
         name="remove_movie"),

    # Rating
    path("thumb-up/<int:movie_id>/", views.thumb_up, name="thumb_up"),
    path("thumb-down/<int:movie_id>/", views.thumb_down, name="thumb_down"),
]
