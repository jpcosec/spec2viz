"""The blog's API under the site root."""

from django.urls import include, path

urlpatterns = [
    path("", include("blog.urls")),
]
