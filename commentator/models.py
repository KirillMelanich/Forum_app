import os
import uuid

from django.db.models import Max
from django.utils.text import slugify

from django.conf import settings
from django.db import models


def post_image_file_path(instance, filename):
    """
    Creates correct image path
    """
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.created_at)}-{uuid.uuid4()}.{extension}"

    return os.path.join(f"uploads/posts_images/", filename)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    email = models.EmailField(max_length=65, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def like(self, user):
        Like.objects.create(user=user, post=self)
        self.likes += 1
        self.save()

    def dislike(self, user):
        Dislike.objects.create(user=user, post=self)
        self.dislikes += 1
        self.save()

    def get_likes_count(self):
        return self.likes

    def get_dislikes_count(self):
        return self.dislikes

    def __str__(self):
        return f"{self.content[:33]}..."


def comment_image_file_path(instance, filename):
    """
    Creates correct image path
    """
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.created_at)}-{uuid.uuid4()}.{extension}"

    return os.path.join(f"uploads/comments_images/", filename)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    image = models.ImageField(null=True, upload_to=comment_image_file_path)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def like(self, user):
        Like.objects.create(user=user, comment=self)
        self.likes += 1
        self.save()

    def dislike(self, user):
        Dislike.objects.create(user=user, comment=self)
        self.dislikes += 1
        self.save()

    def get_likes_count(self):
        return self.likes

    def get_dislikes_count(self):
        return self.dislikes

    def __str__(self):
        return f"{self.content[:12]}...by {self.author.email}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


def profile_image_file_path(instance, filename):
    """
    Creates correct image path
    """
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.registrated_at)}-{uuid.uuid4()}.{extension}"

    return os.path.join(f"uploads/profiles_images/", filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=profile_image_file_path)
    last_activity = models.DateTimeField(null=True, blank=True)
    registrated_at = models.DateTimeField(auto_now_add=True)

    def get_last_activity(self):
        last_post_created_at = Post.objects.filter(author=self.user).aggregate(
            last_post_created_at=Max("created_at")
        )["last_post_created_at"]
        last_comment_created_at = Comment.objects.filter(author=self.user).aggregate(
            last_comment_created_at=Max("created_at")
        )["last_comment_created_at"]
        last_like_created_at = Like.objects.filter(author=self.user).aggregate(
            last_like_created_at=Max("created_at")
        )["last_like_created_at"]
        last_dislike_created_at = Dislike.objects.filter(author=self.user).aggregate(
            last_dislike_created_at=Max("created_at")
        )["last_dislike_created_at"]

        last_action = max(
            last_post_created_at,
            last_comment_created_at,
            last_like_created_at,
            last_dislike_created_at,
        )

        self.last_activity = last_action

        self.save()

    def get_registrated_at(self):
        return self.registrated_at
