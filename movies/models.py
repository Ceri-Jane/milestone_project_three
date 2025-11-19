from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """
    Represents a single movie saved by a user on their personal shelf.
    Stores TMDB ID, title, poster, shelf status, rating, etc.
    """

    STATUS_CHOICES = [
        ("to_watch", "To Watch"),
        ("watched", "Watched"),
        ("to_put_away", "To Put Away"),
    ]

    RATING_CHOICES = [
        ("up", "Thumbs Up"),
        ("down", "Thumbs Down"),
        ("none", "No Rating"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    tmdb_id = models.CharField(max_length=20)
    poster_url = models.URLField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to_watch")
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default="none")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   # ⭐ ADD THIS

    def __str__(self):
        return f"{self.title} ({self.user.username})"
