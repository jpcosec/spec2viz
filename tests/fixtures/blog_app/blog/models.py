"""The posts of the blog and who writes them."""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """A post of the blog."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="posts")
    title = models.CharField(max_length=200)
    body = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "posts"

    def publish(self, by) -> None:
        """Publish the post: it becomes visible to readers."""
        if not can_publish(by, self):
            raise PermissionError("this user may not publish this post")
        self.status = self.Status.PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=["status", "published_at"])


def can_publish(user, post: Post) -> bool:
    """Who may publish a post: its author, or an editor."""
    return user == post.author or user.has_perm("blog.change_post")
