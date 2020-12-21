import os
from django.db import models
from accounts.models import User
from django.utils import timezone

# helper function to build the files name


def upload_to(instance, filename):
    print(instance)
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class Permissions(models.Model):
    perm = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True, default=None)


class ImageRepository(models.Model):
    caption = models.TextField(null=True, blank=True, default=None)
    image_url = models.ImageField(upload_to=upload_to)
    image_type = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
