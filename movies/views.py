import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie


# -------------------------------------------------------------
# HOME PAGE – TMDB SEARCH
# -------------------------------------------------------------
def home(request):
    """
    Displays the search page and calls the TMDB API when the user
    types a search query.
    """
    query = request.GET.get("query", "")
    movies = []

    if not settings.TMDB_API_KEY:
        return render(request, "movies/home.html", {
            "query": query,
            "movies": [],
            "tmdb_error": "TMDB API key is not configured.",
        })

    if query:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "query": query,
            "include_adult": False,
            "language": "en-US",
            "page": 1,
        }

        try:
            response = requests.get(url, params=params, timeout=8)
            data = response.json()
            movies = data.get("results", [])
        except Exception as e:
            print("TMDB ERROR:", e)
            return render(request, "movies/home.html", {
                "query": query,
                "movies": [],
                "tmdb_error": "There was a problem contacting TMDB.",
            })

    return render(request, "movies/home.html", {
        "query": query,
        "movies": movies,
    })


# -------------------------------------------------------------
# USER MOVIE SHELF – GROUPED BY STATUS
# -------------------------------------------------------------
@login_required
def my_shelf(request):
    """
    Displays movies grouped by shelf status:
      - to_put_away
      - to_watch
      - watched
    """

    to_put_away = Movie.objects.filter(user=request.user, status="to_put_away")
    to_watch = Movie.objects.filter(user=request.user, status="to_watch")
    watched = Movie.objects.filter(user=request.user, status="watched")

    return render(request, "movies/shelf.html", {
        "to_put_away": to_put_away,
        "to_watch": to_watch,
        "watched": watched,
    })


# -------------------------------------------------------------
# CHANGE MOVIE STATUS
# -------------------------------------------------------------
@login_required
def change_status(request, movie_id, new_status):
    """
    Updates the status of a movie (to_watch, watched, to_put_away).
    """
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)

    VALID_STATUSES = ["to_watch", "watched", "to_put_away"]

    if new_status not in VALID_STATUSES:
        return redirect("my_shelf")

    movie.status = new_status
    movie.save()

    return redirect("my_shelf")


# -------------------------------------------------------------
# REMOVE MOVIE FROM USER'S SHELF
# -------------------------------------------------------------
@login_required
def remove_movie(request, movie_id):
    """
    Deletes a movie from the user's saved shelf.
    """
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    movie.delete()
    return redirect("my_shelf")


# -------------------------------------------------------------
# RATING – THUMBS UP
# -------------------------------------------------------------
@login_required
def thumb_up(request, movie_id):
    """
    Sets rating to 'up' for a movie.
    """
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    movie.rating = "up"
    movie.save()
    return redirect("my_shelf")


# -------------------------------------------------------------
# RATING – THUMBS DOWN
# -------------------------------------------------------------
@login_required
def thumb_down(request, movie_id):
    """
    Sets rating to 'down' for a movie.
    """
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    movie.rating = "down"
    movie.save()
    return redirect("my_shelf")
