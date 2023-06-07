from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to="media/post_image/", blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
        related_name="post"
    )

    class Meta:
        ordering = ["created_time"]

    _metadata = {
        "post_image": "get_meta_image",
    }

    def get_meta_image(self):
        if self.post_image:
            return self.post_image.url

    def __str__(self) -> str:
        return f"{self.title} | {self.owner.name}"


class Commentary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        name="user",
        related_name="commentaries",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        name="post",
        related_name="commentaries",
    )
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    commentary_image = models.ImageField(upload_to="media/commentaries_image/", blank=True)

    class Meta:
        ordering = ["created_time"]

    _metadata = {
        "commentaries_image": "get_meta_image",
    }

    def get_meta_image(self):
        if self.commentary_image:
            return self.commentary_image.url


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        unique=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to="media/profile_pictures/", blank=True)
