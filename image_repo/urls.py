from django.urls import path

from . import views

urlpatterns = [
    path('permissions', views.PermissionAPIVIew.as_view()),
    path('repositories', views.RepositoryAPIView.as_view()),
    path('repositories/<int:pk>', views.RepositoryAPIView.as_view()),
    path('repositories/<int:repository_id>/images/<int:pk>',
         views.DeleteImageAPIView.as_view()),
    path('repositories/<int:repository_id>/images',
         views.DeleteImagesAPIView.as_view()),
]
