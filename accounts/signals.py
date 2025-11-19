from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import GroupProfile  # NEW

User = get_user_model()

# Auto-assign normal users to "Site Users"
@receiver(post_save, sender=User)
def add_to_site_users_group(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        group, _ = Group.objects.get_or_create(name="Site Users")
        instance.groups.add(group)


# Auto-create a GroupProfile whenever a new Group is created
@receiver(post_save, sender=Group)
def create_group_profile(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)
