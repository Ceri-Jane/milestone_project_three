from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class GroupProfile(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name="profile"
    )
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.group.name} Profile"


# ----------------------------------------------------------
# AUTO-ASSIGN NEW USERS TO "Site Users" GROUP
# ----------------------------------------------------------
@receiver(post_save, sender='auth.User')
def add_new_user_to_site_users(sender, instance, created, **kwargs):
    """
    Automatically assigns every newly registered user
    to the 'Site Users' group.
    """

    if not created:  # Only on first creation
        return

    # Get or create the group
    group, _ = Group.objects.get_or_create(name="Site Users")

    # Ensure the group has a profile (optional, for your admin)
    GroupProfile.objects.get_or_create(
        group=group,
        defaults={"description": "Normal website users"}
    )

    # Assign user to group
    instance.groups.add(group)
