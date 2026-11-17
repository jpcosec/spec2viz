"""The router of the blog's API: /posts/ and /posts/{id}/publish."""

from rest_framework.routers import SimpleRouter

from blog.views import PostViewSet

router = SimpleRouter(trailing_slash=False)
router.register("posts", PostViewSet, basename="post")

urlpatterns = router.urls
