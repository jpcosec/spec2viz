"""How a post goes over the API."""

from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "body", "status", "published_at"]
        read_only_fields = ["author", "status", "published_at"]
