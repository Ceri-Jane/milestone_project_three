"""
URL configuration for the quickflicks project.

This file defines the top-level URL routes for the project.
Each path maps a URL to a specific view function. Views return
the response that is displayed in the user's browser.

As the project grows, individual apps (e.g. accounts, movies)
will have their own URL files which we include from here.
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import render   # used for rendering HTML templates

# Home page view
# This function loads the home.html template and returns it to the browser.
# Using render() allows us to return full HTML templates instead of plain text.
def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL of the project. When a user visits "/", this view is displayed.
    path('', home, name='home'),
]
