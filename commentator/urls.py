from django.urls import path, include
from rest_framework.routers import DefaultRouter

from commentator.views import PostViewSet, CommentViewSet, ProfileViewSet

routers = DefaultRouter()

routers.register("posts", PostViewSet, basename="posts")
routers.register("comments", CommentViewSet, basename="comments")
routers.register("profiles", ProfileViewSet, basename="profiles")


urlpatterns = [
    path("", include(routers.urls)),
]

app_name = "commentator"
