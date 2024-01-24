from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like, Dislike, Profile
from .serializers import PostSerializer, CommentSerializer, ProfileSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=["post"])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                post=parent_comment.post,
                author=request.user,
                parent_comment=parent_comment,
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user

        # Check if the user has already disliked the comment
        if Dislike.objects.filter(user=user, comment=comment).exists():
            comment.likes -= 1
            Dislike.objects.filter(user=user, comment=comment).delete()

        # Check if the user has already liked the comment
        elif Like.objects.filter(user=user, comment=comment).exists():
            return Response(
                {"detail": "You have already liked this comment before"},
                status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.create(user=user, comment=comment)
        comment.likes += 1
        comment.save()

        return Response(
            {"detail": "Comment liked successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def dislike(self, request, pk=None):
        comment = self.get_object()
        user = request.user

        # Check if the user has already liked the comment
        if Like.objects.filter(user=user, comment=comment).exists():
            comment.likes -= 1
            Like.objects.filter(user=user, comment=comment).delete()

        # Check if the user has already disliked the comment
        elif Dislike.objects.filter(user=user, comment=comment).exists():
            return Response(
                {"detail": "You have already disliked this post before"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Dislike.objects.create(user=user, comment=comment)
        comment.dislikes += 1
        comment.save()

        return Response(
            {"detail": "Comment disliked successfully."}, status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Check if the user has already disliked the post
        if Dislike.objects.filter(user=user, post=post).exists():
            post.dislikes -= 1
            Dislike.objects.filter(user=user, post=post).delete()

        # Check if the user has already liked the post
        elif Like.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already liked this post before"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.create(user=user, post=post)
        post.likes += 1
        post.save()

        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Check if user has already liked this post
        if Like.objects.filter(user=user, post=post).exists():
            post.likes -= 1
            Like.objects.filter(user=user, post=post).delete()

        # Check if user has already disliked this post
        elif Dislike.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already disliked this post before"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Dislike.objects.create(user=user, post=post)
        post.dislikes += 1
        post.save()

        return Response(
            {"detail": "Post disliked successfully."}, status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        # Set the user of the profile to the authenticated user making the request
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["put"])
    def update_image(self, request, pk=None):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
