from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permissions
        fields = '__all__'


class ImageRepositorySerializer(serializers.ModelSerializer):
    owner_info = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = models.ImageRepository
        fields = ('id', 'caption', 'image_url', 'image_type',
                  'owner', 'owner_info', 'permission', 'created_at')
