from django.contrib.auth.models import Group
from django.db import models

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="profile")
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.group.name} Profile"
