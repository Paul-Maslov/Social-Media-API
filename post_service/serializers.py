from rest_framework import serializers

from post_service.models import Commentary, Post


class CommentaryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commentary
        fields = (
            "id",
            "user",
            "content",
            "created_time",
            "commentary_image"
        )


class PostSerializer(serializers.ModelSerializer):
    commentaries = CommentaryListSerializer(
        many=True,
        read_only=False,
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "content",
            "created_time",
            "post_image"
        )
