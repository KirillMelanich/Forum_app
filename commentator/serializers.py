from rest_framework import serializers
from .models import Post, Comment, Profile, Like, Dislike


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
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "created_at",
            "image",
            "content",
            "likes",
            "dislikes",
            "parent_comment",
            "replies",
        )
        read_only_fields = ("author",)

    @staticmethod
    def get_likes(obj):
        return obj.get_likes_count()

    @staticmethod
    def get_dislikes(obj):
        return obj.get_dislikes_count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally include "parent_comment" and "replies" and "image" if not empty
        if not instance.parent_comment:
            representation.pop("parent_comment")
        if not instance.replies.exists():
            representation.pop("replies")
        if not instance.image:
            representation.pop("image")

        return representation


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    num_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "created_at",
            "image",
            "content",
            "likes",
            "dislikes",
            "num_of_comments",
            "comments",
        )
        read_only_fields = ("comments", "author")

    @staticmethod
    def get_likes(obj):
        return obj.get_likes_count()

    @staticmethod
    def get_dislikes(obj):
        return obj.get_dislikes_count()

    @staticmethod
    def get_author(obj):
        return obj.author.id

    @staticmethod
    def get_num_of_comments(obj):
        return obj.comments.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally exclude "comments" and "image" if empty or None
        if not instance.comments.exists():
            representation.pop("comments", None)
        if not instance.image:
            representation.pop("image")

        return representation


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    registrated_at = serializers.DateTimeField(read_only=True)
    posts_made = serializers.SerializerMethodField()
    comments_made = serializers.SerializerMethodField()
    likes_given = serializers.SerializerMethodField()
    dislikes_given = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "user_id",
            "user_name",
            "image",
            "registrated_at",
            "last_activity",
            "posts_made",
            "comments_made",
            "likes_given",
            "dislikes_given",
        )
        read_only_fields = (
            "user_id",
            "user_name",
            "registrated_at",
            "last_activity",
            "posts_made",
            "comments_made",
            "likes_given",
            "dislikes_given",
        )

    @staticmethod
    def get_posts_made(profile):
        return Post.objects.filter(author=profile.user).count()

    @staticmethod
    def get_comments_made(profile):
        return Comment.objects.filter(author=profile.user).count()

    @staticmethod
    def get_likes_given(profile):
        return Like.objects.filter(user=profile.user).count()

    @staticmethod
    def get_dislikes_given(profile):
        return Dislike.objects.filter(user=profile.user).count()
