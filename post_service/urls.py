from django.urls import path, include
from rest_framework import routers

from post_service.views import (
    PostListViewSet,
    UserViewSet,
    PostDetailAPIView,
    UpvoteAPIView,
    CommentAPIView,
)

router = routers.DefaultRouter()
router.register("posts", PostListViewSet)
router.register("users", UserViewSet)


urlpatterns = [
    path("posts/<int:pk>/upvote/", UpvoteAPIView.as_view()),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("posts/<int:pk>/comment/", CommentAPIView.as_view()),
    path("", include(router.urls)),
]

app_name = "post_service"
