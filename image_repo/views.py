from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers


class PermissionAPIVIew(generics.ListAPIView):
    queryset = models.Permissions.objects.all()
    serializer_class = serializers.PermissionSerializer


class ImageRepositoryAPIView(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = models.ImageRepository.objects.all()
    serializer_class = serializers.ImageRepositorySerializer
