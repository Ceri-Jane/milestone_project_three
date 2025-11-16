"""
URL configuration for the quickflicks project.

This file defines the top-level URL routes for the project.
Each path maps a URL to a specific view function. Views return
the response that is displayed in the user's browser.

As the project grows, individual apps (e.g. accounts, movies)
will have their own URL files which we include from here.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("movies.urls")),  # home + search
]
