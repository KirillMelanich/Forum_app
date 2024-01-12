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

    def __str__(self):
        return f"{self.content[:33]}..."


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home_page = models.URLField(max_length=255, null=True, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'{self.content[:12]}...by {self.author.email}'
