from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    # -------- LIST VIEW DISPLAY --------
    list_display = (
        "thumbnail",
        "title",
        "user",
        "status_badge",
        "rating_display",
        "tmdb_id",
        "created_at",
    )

    list_filter = ("status", "rating", "user", "created_at")
    search_fields = ("title", "tmdb_id", "user__username")
    ordering = ("-created_at",)

    fieldsets = (
        ("Movie Information", {
            "fields": ("title", "tmdb_id", "poster_url")
        }),
        ("Shelf Status", {
            "fields": ("user", "status", "rating")
        }),
        ("Timestamp", {
            "fields": ("created_at",),
        }),
    )

    readonly_fields = ("created_at",)

    # -------- CUSTOM DISPLAY METHODS --------
    def thumbnail(self, obj):
        url = (obj.poster_url or "").strip()

        if not url or url.endswith("None") or not (url.startswith("http://") or url.startswith("https://")):
            url = static("images/movie-poster-unavailable.jpg")

        return format_html(
            '<img src="{}" style="height:60px; border-radius:4px;" />',
            url,
        )
    thumbnail.short_description = "Poster"

    def rating_display(self, obj):
        return {"up": "👍", "down": "👎", "none": "Not rated"}.get(obj.rating, "Not rated")
    rating_display.short_description = "Rating"

    def status_badge(self, obj):
        color_map = {
            "to_put_away": "gray",
            "to_watch": "#007bff",
            "watched": "green",
        }
        color = color_map.get(obj.status, "gray")
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            obj.get_status_display(),
        )
    status_badge.short_description = "Status"
