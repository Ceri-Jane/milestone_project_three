import requests
from django.conf import settings
from django.shortcuts import render, HttpResponse


def home(request):
    query = request.GET.get("query", "")
    movies = []

    # Prevent crashes if API key is missing
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
