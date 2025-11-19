from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from movies.models import Movie
from .models import GroupProfile


# -----------------------------
# USER ADMIN CUSTOMISATIONS
# -----------------------------

def group_list(obj):
    """Show comma-separated group names."""
    return ", ".join([g.name for g in obj.groups.all()]) or "—"
group_list.short_description = "Groups"


def total_movies(obj):
    """Clickable count → takes admin to filtered Movie list."""
    count = Movie.objects.filter(user=obj).count()

    url = (
        reverse("admin:movies_movie_changelist")
        + "?"
        + urlencode({"user__id__exact": obj.id})
    )

    return format_html('<a href="{}">{}</a>', url, count)
total_movies.short_description = "Movies"


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        group_list,
        total_movies,
    )

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -----------------------------
# GROUP ADMIN CUSTOMISATIONS
# -----------------------------

def member_count(obj):
    """Clickable number showing how many users in the group."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    count = User.objects.filter(groups=obj).count()

    url = (
        reverse("admin:auth_user_changelist")
        + "?"
        + urlencode({"groups__id__exact": obj.id})
    )
    return format_html('<a href="{}">{}</a>', url, count)
member_count.short_description = "Members"


def total_permissions(obj):
    return obj.permissions.count()
total_permissions.short_description = "Permissions"


class CustomGroupAdmin(admin.ModelAdmin):
    """
    Clean Group admin — shows description but does NOT create/modify profiles.
    Creation is handled by signals to avoid duplicate GroupProfile rows.
    """
    list_display = ("name", member_count, total_permissions, "get_description")

    def get_description(self, obj):
        return getattr(obj.profile, "description", "")
    get_description.short_description = "Description"


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
