"""The posts endpoints."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from blog.models import Post
from blog.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None) -> Response:
        """POST /posts/{id}/publish: publish one post."""
        post = self.get_object()
        try:
            post.publish(by=request.user)
        except PermissionError as error:
            raise PermissionDenied(str(error)) from error
        return Response(PostSerializer(post).data)
