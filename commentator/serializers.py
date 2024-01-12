from rest_framework import serializers
from captcha.fields import CaptchaField
from .models import Post, Comment


class RecursiveSerializer(serializers.Serializer):
    """For Recursive representation of comments"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    """Lists comments only under parents comment"""
    def to_representation(self, data):
        data = data.filter(parent_comment=None)
        return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    captcha = CaptchaField()
    replies = RecursiveSerializer(many=True, required=False)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Comment
        fields = (
            "id",
            "author",
            "home_page",
            "post",
            "content",
            "created_at",
            "parent_comment",
            "replies",
        )
        read_only_fields = ("author",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally include "parent_comment" and "replies" and "home_page" if not empty
        if not instance.parent_comment:
            representation.pop("parent_comment")
        if not instance.replies.exists():
            representation.pop("replies")
        if not instance.home_page:
            representation.pop("home_page", None)

        return representation


class PostSerializer(serializers.ModelSerializer):
    captcha = CaptchaField()
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "home_page", "content", "created_at", "comments")
        read_only_fields = ("comments", "author")

    @staticmethod
    def get_author(obj):
        return obj.author.id

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally exclude "comments" and "home_page" if empty or None
        if not instance.comments.exists():
            representation.pop("comments", None)

        if not instance.home_page:
            representation.pop("home_page", None)

        return representation

