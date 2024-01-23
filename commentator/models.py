from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    email = models.EmailField(max_length=65, null=False, blank=False)
    home_page = models.URLField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False, null=False)
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


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home_page = models.URLField(max_length=255, null=True, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
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
        return f'{self.content[:12]}...by {self.author.email}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     country = models.CharField(max_length=255, unique=False, blank=True, null=True)
#     city = models.CharField(max_length=255, unique=False, blank=True, null=True)
#     registration_time = models.DateTimeField(auto_now_add=True)