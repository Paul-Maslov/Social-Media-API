from django.conf import settings

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to="media/post_image/", blank=True)
    upvote_count = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="post",
    )

    class Meta:
        ordering = ["created_time"]

    _metadata = {
        "post_image": "get_meta_image",
    }

    @property
    def amount_commentaries(self):
        return self.commentaries.count()

    def get_meta_image(self):
        if self.post_image:
            return self.post_image.url

    def __str__(self) -> str:
        return f"{self.title} | {self.user}"


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
    commentary_image = models.ImageField(
        upload_to="media/commentaries_image/", blank=True
    )

    class Meta:
        ordering = ["created_time"]

    _metadata = {
        "commentaries_image": "get_meta_image",
    }

    def get_meta_image(self):
        if self.commentary_image:
            return self.commentary_image.url

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        unique=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(
        upload_to="media/profile_pictures/",
        blank=True
    )
    following = models.ManyToManyField(
        "UserProfile",
        related_name="follow_for"
    )
    followers = models.ManyToManyField(
        "UserProfile",
        related_name="follow_at"
    )
    posts = models.ManyToManyField(Post, related_name="posts")

    class Meta:
        ordering = ["name"]

    _metadata = {
        "picture": "get_meta_image",
    }

    def get_meta_image(self):
        if self.picture:
            return self.picture.url

    @property
    def amount_followers(self):
        return self.followers.count()

    @property
    def amount_following(self):
        return self.following.count()


class Upvote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="upvotes",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name="upvotes",
        on_delete=models.CASCADE
    )
