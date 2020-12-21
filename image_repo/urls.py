from django.urls import path

from . import views

urlpatterns = [
    path('permissions', views.PermissionAPIVIew.as_view()),
    # path('permissions/<pk>', views.PermissionAPIVIew.as_view()),
    path('image/repository', views.ImageRepositoryAPIView.as_view())
]
