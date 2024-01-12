from captcha.models import CaptchaStore
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        # Validate captcha only if the user is not an admin
        if not self.request.user.is_staff:
            captcha_value = self.request.data.get("captcha")
            captcha_id = self.request.data.get("captcha_0")

            if not CaptchaStore.objects.filter(response=captcha_value, hashkey=captcha_id).exists():
                raise ValidationError({"captcha": "Invalid captcha."})

        serializer.save(author_id=self.request.user.id)

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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # Validate captcha only if the user is not an admin
        if not self.request.user.is_staff:
            captcha_value = self.request.data.get("captcha")
            captcha_id = self.request.data.get("captcha_0")

            if not CaptchaStore.objects.filter(response=captcha_value, hashkey=captcha_id).exists():
                raise ValidationError({"captcha": "Invalid captcha."})

        serializer.save(author_id=self.request.user.id)

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
