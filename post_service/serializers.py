from rest_framework import serializers

from post_service.models import Commentary, Post, UserProfile, Upvote


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ("id", "user", "post")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "name",
            "bio",
            "birth_date",
            "location",
            "picture",
            "amount_followers",
            "amount_following",
        )


class UserListSerializer(UserSerializer):
    amount_posts = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "name",
            "picture",
            "amount_posts",
            "amount_followers",
            "amount_following",
        )

    def get_amount_posts(self, obj: UserProfile):
        return Post.objects.filter(id=obj.id).count()


class CommentaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "id",
            "user"
            "content",
            "post",
            "created_time",
            "commentary_image"
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "content",
            "created_time",
            "post_image",
        )


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + (
            "amount_commentaries",
            "upvote_count"
        )
        read_only_fields = ("upvote_count", "amount_commentaries")


class PostDetailSerializer(PostListSerializer):
    commentaries = CommentaryListSerializer(
        many=True,
    )

    class Meta:
        model = Post
        fields = PostListSerializer.Meta.fields + ("commentaries",)


class UserDetailSerializer(UserSerializer):
    following = UserSerializer(many=True)
    followers = UserSerializer(many=True)
    posts = PostSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ("id", "name", "following", "followers", "posts")
