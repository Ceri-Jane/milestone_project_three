from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    # -------- LIST VIEW --------
    list_display = (
        "thumbnail",
        "title",
        "user",
        "status_badge",
        "rating_display",
        "tmdb_id",
        "created_at",
    )

    list_display_links = ("title",)  # clickable title

    list_filter = (
        "status",
        "rating",
        "user",
        "created_at",
    )

    search_fields = (
        "title__icontains",
        "tmdb_id",
        "user__username",
    )

    ordering = ("-created_at",)

    # -------- FIELDSET LAYOUT --------
    fieldsets = (
        ("Movie Information", {
            "fields": ("title", "tmdb_id", "poster_url")
        }),
        ("Shelf & Status", {
            "fields": ("user", "status", "rating")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    # -------- CUSTOM COLUMNS --------

    def release_year(self, obj):
        if hasattr(obj, "release_date") and obj.release_date:
            return obj.release_date[:4]
        return "—"
    release_year.short_description = "Year"

    def thumbnail(self, obj):
        """Show TMDB poster OR fallback image."""
        url = (obj.poster_url or "").strip()

        if not url or url.endswith("None"):
            url = ""

        if url.startswith("http://") or url.startswith("https://"):
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px;" />',
                url
            )

        fallback_url = static("images/movie-poster-unavailable.jpg")
        return format_html(
            '<img src="{}" style="height:60px; border-radius:4px; opacity:0.9;" />',
            fallback_url
        )

    thumbnail.short_description = "Poster"
    
    def rating_display(self, obj):
        if obj.rating == "up":
            return "👍"
        elif obj.rating == "down":
            return "👎"
        return "Not yet rated"
    
    rating_display.short_description = "Rating"

    def status_badge(self, obj):
        color_map = {
            "NEW": "gray",
            "TO_WATCH": "blue",
            "WATCHED": "green",
        }
        color = color_map.get(obj.status, "gray")
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    # -------- ADMIN ACTIONS --------

    @admin.action(description="Mark selected movies as Watched")
    def mark_watched(self, request, queryset):
        queryset.update(status="WATCHED")

    @admin.action(description="Reset rating to 'Not rated'")
    def reset_rating(self, request, queryset):
        queryset.update(rating=0)

    actions = [mark_watched, reset_rating]

    # -------- READ-ONLY WHEN WATCHED --------
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == "WATCHED":
            return ("title", "tmdb_id", "poster_url", "created_at", "updated_at")
        return self.readonly_fields
