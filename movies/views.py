import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie


# -------------------------------------------------------------
# HOME PAGE – TMDB SEARCH + "Add to Shelf" Support
# -------------------------------------------------------------
def home(request):
    """
    Displays the search page, calls the TMDB API when the user
    searches, and also checks which movies the user already saved.
    """
    query = request.GET.get("query", "")
    movies = []

    # If no TMDB key → avoid crash
    if not settings.TMDB_API_KEY:
        return render(request, "movies/home.html", {
            "query": query,
            "movies": [],
            "tmdb_error": "TMDB API key is not configured.",
        })

    # If user typed a query → call TMDB API
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

    # ---------------------------------------------------------
    # If logged in → get IDs of movies already in the shelf
    # so the template knows when to show "Already in shelf"
    # ---------------------------------------------------------
    user_movie_ids = []
    if request.user.is_authenticated:
        user_movie_ids = list(
            Movie.objects.filter(user=request.user).values_list("tmdb_id", flat=True)
        )

    return render(request, "movies/home.html", {
        "query": query,
        "movies": movies,
        "user_movie_ids": user_movie_ids,
    })


# -------------------------------------------------------------
# ADD MOVIE TO SHELF
# -------------------------------------------------------------
@login_required
def add_to_shelf(request):
    """
    Adds a movie to the user's personal shelf.
    Called from the home page search results.
    """
    if request.method == "POST":
        tmdb_id = request.POST.get("tmdb_id")
        title = request.POST.get("title")
        poster_path = request.POST.get("poster_path")

        # Create movie only if not already saved
        Movie.objects.get_or_create(
            user=request.user,
            tmdb_id=tmdb_id,
            defaults={
                "title": title,
                "poster_url": (
                    f"https://image.tmdb.org/t/p/w300{poster_path}"
                    if poster_path else ""
                ),
                "status": "to_put_away",
            }
        )

    # Return user to the page they came from
    return redirect(request.META.get("HTTP_REFERER", "home"))


# -------------------------------------------------------------
# USER MOVIE SHELF – GROUPED BY STATUS
# -------------------------------------------------------------
@login_required
def my_shelf(request):
    """
    Displays user's movies grouped by:
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
    Updates the movie's status:
      - to_put_away
      - to_watch
      - watched
    """
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)

    VALID_STATUSES = ["to_put_away", "to_watch", "watched"]

    if new_status in VALID_STATUSES:
        movie.status = new_status
        movie.save()

    return redirect("my_shelf")


# -------------------------------------------------------------
# REMOVE MOVIE FROM SHELF
# -------------------------------------------------------------
@login_required
def remove_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    movie.delete()
    return redirect("my_shelf")


# -------------------------------------------------------------
# RATING – THUMBS UP / DOWN
# -------------------------------------------------------------
@login_required
def thumb_up(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    movie.rating = "up"
    movie.save()
    return redirect("my_shelf")


@login_required
def thumb_down(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    movie.rating = "down"
    movie.save()
    return redirect("my_shelf")
