from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # User shelf
    path("my-shelf/", views.my_shelf, name="my_shelf"),

    # Change movie status (to_watch, watched, to_put_away)
    path(
        "change-status/<int:movie_id>/<str:new_status>/",
        views.change_status,
        name="change_status"
    ),

    # Remove movie from shelf
    path(
        "remove-movie/<int:movie_id>/",
        views.remove_movie,
        name="remove_movie"
    ),

    # Rating (thumb up / down)
    path(
        "thumb-up/<int:movie_id>/",
        views.thumb_up,
        name="thumb_up"
    ),
    path(
        "thumb-down/<int:movie_id>/",
        views.thumb_down,
        name="thumb_down"
    ),
]
