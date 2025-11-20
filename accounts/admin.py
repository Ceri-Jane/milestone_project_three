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
    return ", ".join([g.name for g in obj.groups.all()]) or "—"
group_list.short_description = "Groups"


def total_movies(obj):
    count = Movie.objects.filter(user=obj).count()
    url = (
        reverse("admin:movies_movie_changelist")
        + "?"
        + urlencode({"user__id__exact": obj.id})
    )
    return format_html('<a href="{}">{}</a>', url, count)
total_movies.short_description = "Movies"


class CustomUserAdmin(UserAdmin):
    """
    Custom version of Django's UserAdmin.
    Removes first_name and last_name fields from the admin form.
    """

    # ---- REMOVE FIRST & LAST NAME FROM FIELDSETS ----
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),  # first_name/last_name REMOVED
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = (
        "username", "email", "is_active", "is_staff",
        "is_superuser", group_list, total_movies,
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")


# Unregister default and register custom
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -----------------------------
# GROUP ADMIN CUSTOMISATIONS
# -----------------------------

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    fields = ("description",)
    verbose_name = "Description"
    verbose_name_plural = "Group Description"


class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "member_count", "total_permissions", "get_description")
    inlines = [GroupProfileInline]

    def member_count(self, obj):
        UserModel = admin.site._registry[User].model
        return UserModel.objects.filter(groups=obj).count()
    member_count.short_description = "Members"

    def total_permissions(self, obj):
        return obj.permissions.count()
    total_permissions.short_description = "Permissions"

    def get_description(self, obj):
        return getattr(obj.profile, "description", "")
    get_description.short_description = "Description"


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
