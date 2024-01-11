from rest_framework import serializers
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

    replies = RecursiveSerializer(many=True, required=False)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "content",
            "created_at",
            "parent_comment",
            "replies",
        )
        read_only_fields = ("author",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally include "parent_comment" and "replies" if not empty
        if not instance.parent_comment:
            representation.pop("parent_comment")
        if not instance.replies.exists():
            representation.pop("replies")

        return representation


class PostSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "content", "created_at", "comments"]
        read_only_fields = ("comments", "author")

    @staticmethod
    def get_author(obj):
        return obj.author.id
