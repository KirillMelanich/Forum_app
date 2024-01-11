from django.urls import path, include
from rest_framework.routers import DefaultRouter

from commentator.views import PostViewSet, CommentViewSet

routers = DefaultRouter()

routers.register("posts", PostViewSet, basename="posts")
routers.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("", include(routers.urls)),
]

app_name = "commentator"
