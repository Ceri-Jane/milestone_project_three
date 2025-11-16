import requests
from django.conf import settings
from django.shortcuts import render

def home(request):
    query = request.GET.get("query", "")  # read search bar input
    movies = []

    if query:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "query": query,
            "include_adult": False,
            "language": "en-US",
            "page": 1,
        }
        response = requests.get(url, params=params)
        data = response.json()

        movies = data.get("results", [])

    context = {
        "query": query,
        "movies": movies,
    }

    return render(request, "movies/home.html", context)
