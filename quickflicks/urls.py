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
from django.shortcuts import render       # used for rendering HTML templates

# Home page view
def home(request):
    return render(request, "movies/home.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts URLs (login, signup, etc.)
    path('accounts/', include('accounts.urls')),
    
    # Root URL
    path('', home, name='home'),
]