import requests
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie


# -------------------------------------------------------------
# HOME PAGE: Search TMDB for movies using user query
# -------------------------------------------------------------
def home(request):
    # Pull the search query from the URL (?query=something)
    query = request.GET.get("query", "")
    movies = []

    # If the TMDB API key is missing, we avoid crashing the whole site
    if not settings.TMDB_API_KEY:
        return render(request, "movies/home.html", {
            "query": query,
            "movies": [],
            "tmdb_error": "TMDB API key is not configured.",
        })

    # If the user has typed something, call the TMDB API
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
            # Make request to TMDB
            response = requests.get(url, params=params, timeout=8)
            data = response.json()

            # Extract the movie results list
            movies = data.get("results", [])

        except Exception as e:
            # Any TMDB failure (timeout, JSON error, rate-limit, etc.)
            print("TMDB ERROR:", e)
            return render(request, "movies/home.html", {
                "query": query,
                "movies": [],
                "tmdb_error": "There was a problem contacting TMDB.",
            })

    # Render homepage with either an empty list or real search results
    return render(request, "movies/home.html", {
        "query": query,
        "movies": movies,
    })


# -------------------------------------------------------------
# USER'S PERSONAL MOVIE SHELF
# Displays movies saved to the user's account
# -------------------------------------------------------------
@login_required
def my_shelf(request):
    """
    This view displays all movies the logged-in user has stored
    in their personal movie shelf.

    @login_required:
        Ensures only authenticated users can view their shelf.

    Queryset:
        Filters Movie objects by the 'user' who owns them.
        Orders results so the newest saved movies appear first.

    Template:
        Renders 'movies/shelf.html' with the user's movies.
    """

    # Filter Movie table by the logged-in user ONLY
    movies = Movie.objects.filter(user=request.user).order_by("-created_at")

    # Render the shelf page with the user's saved movies
    return render(request, "movies/shelf.html", {
        "movies": movies
    })
