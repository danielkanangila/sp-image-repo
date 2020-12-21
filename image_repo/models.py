import os
from django.db import models
from accounts.models import User
from django.utils import timezone

# helper function to build the files name


def upload_to(instance, filename):
    user_id = instance.repository.owner.pk
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/users/{user_id}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class Permissions(models.Model):
    perm = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True, default=None)


class Repository(models.Model):
    caption = models.TextField(null=True, blank=True, default=None)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self):
        images = RepositoryImages.objects.filter(repository=self)

        for image in images:
            image.image.delete(save=False)  # delete file in the S3 bucket
            image.delete()  # delete model instance
        super(Repository, self).delete()


class RepositoryImages(models.Model):
    repository = models.ForeignKey(
        Repository, related_name='repository', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)
    image_type = models.CharField(
        max_length=50, null=True, blank=True, default=None)

    def delete(self):
        self.image.delete(save=False)
        super(RepositoryImages, self).delete()
