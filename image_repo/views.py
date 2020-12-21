from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from . import models
from . import serializers


class PermissionAPIVIew(generics.ListAPIView):
    queryset = models.Permissions.objects.all()
    serializer_class = serializers.PermissionSerializer


class ImageRepositoryAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, *args, **kwargs):
        # get form data from request and pass it to serializer for validation
        form_serializer = serializers.RepoFormSerializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)
        # get the validated data
        form_data = form_serializer.validated_data
        # create repository
        repo = self.create_repository(request, form_data)

        # saves images
        self.save_images(images=form_data.get('images'), repository=repo)

        # return the saved data
        return Response(serializers.RepositorySerializer(instance=repo).data)

    def create_repository(self, request, validated_data):
        try:
            repository_data = {
                "caption": validated_data.get('caption'),
                "owner": request.user.pk,
                "permission": validated_data.get('permission')
            }
            serializer = serializers.RepositorySerializer(data=repository_data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except Exception as e:
            print(e)
            raise APIException(
                "An error occurred while trying to save repository.")

    def save_images(self, images, repository):
        try:
            # create a list of image data to be saved
            _images = []
            for image in images:
                image_data = {
                    "repository": repository.pk,
                    "image": image,
                    "image_type": image.content_type
                }
                _images.append(image_data)
            # initialize the serializer with the saved data
            serializer = serializers.RepoImagesSerializer(
                data=_images, many=True)
            # validate data, raise exception if error
            serializer.is_valid(raise_exception=True)
            # save images and return the saved images
            return serializer.save()
        except Exception as e:
            print(e)
            # delete the new created repo if error
            repo.delete()
            # raise an exception
            raise APIException(
                "Repo creation unsuccessful. An error occurred while trying to save images")
