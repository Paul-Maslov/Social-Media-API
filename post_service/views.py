from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from post_service.models import Post, Commentary, UserProfile, Upvote
from post_service.serializers import (
    CommentaryListSerializer,
    PostListSerializer,
    PostSerializer,
    PostDetailSerializer,
    UserSerializer,
    UserDetailSerializer,
    UserListSerializer,
)


class PostPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 100


class PostListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = (
        Post.objects.select_related("user")
        .prefetch_related("commentaries")
        .order_by("created_time")
    )
    serializer_class = PostListSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer

        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(APIView):
    queryset = (
        Post.objects.prefetch_related("commentaries")
        .select_related("user")
        .order_by("created_time")
    )
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        data = {
            "title": request.data.get("title"),
            "content": request.data.get("content"),
            "upvote_count": post.upvote_count,
            "user": request.user.id,
        }
        serializer = PostDetailSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            if post.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "You are not authorized to edit this post"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if post.user.id == request.user.id:
            post.delete()
            return Response(
                {"res": "Object deleted!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "You are not authorized to delete this post"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class CommentAPIView(APIView):
    queryset = Commentary.objects.select_related("post")
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        comments = Commentary.objects.filter(post=post)
        serializer = CommentaryListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        data = {
            "user": request.user.id,
            "post": post.id,
            "content": request.data.get("content"),
            "created_time": request.data.get("created_time"),
            "commentary_image": request.data.get("commentary_image"),
        }
        serializer = CommentaryListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().prefetch_related(
        "following", "followers", "posts"
    )
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action == "retrieve":
            return UserDetailSerializer

        return UserSerializer

    @action(
        methods=["GET"],
        detail=True,
    )
    def follow_toggle(self, request, *args, **kwargs):
        profile = self.get_object()
        follower = request.user.profile
        if profile.followers.filter(pk=follower.pk).exists():
            profile.followers.remove(follower)
            follower.following.remove(profile)
        else:
            profile.followers.add(follower)
            follower.following.add(profile)
        return Response(status=status.HTTP_200_OK)


class UpvoteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        upvoters = post.upvotes.all().values_list("user", flat=True)
        if request.user.id in upvoters:
            post.upvote_count -= 1
            post.upvotes.filter(user=request.user).delete()
        else:
            post.upvote_count += 1
            upvote = Upvote(user=request.user, post=post)
            upvote.save()
            post.save()
        return Response(status=status.HTTP_200_OK)
