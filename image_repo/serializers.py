from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permissions
        fields = '__all__'


class RepoImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RepositoryImages
        fields = '__all__'
        extra_kwargs = {
            "repository": {"write_only": True}
        }


class RepositorySerializer(serializers.ModelSerializer):
    owner_info = UserSerializer(source='owner', read_only=True)
    images = RepoImagesSerializer(
        source="repository", many=True, read_only=True)

    class Meta:
        model = models.Repository
        fields = ['id', 'caption',
                  'owner', 'owner_info', 'permission', 'images', 'created_at']
        extra_kwargs = {
            "owner": {"write_only": True}
        }


# validator of permission field.


def is_valid_permission(pk):
    try:
        permission = models.Permissions.objects.get(
            pk=pk)
        return pk
    except Exception:
        raise serializers.ValidationError("Invalid Permission.")


class RepoFormSerializer(serializers.Serializer):
    caption = serializers.CharField()
    permission = serializers.IntegerField(validators=[is_valid_permission])
    images = serializers.ListField(child=serializers.ImageField())
