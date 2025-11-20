# ---------------------------------------------------------------
# MOVIES APP CONFIG
# - Registers the 'movies' app with Django’s application registry.
# - Sets BigAutoField as the default primary key type for models.
# - Used by Django to identify and configure this app at startup.
# ---------------------------------------------------------------

from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
