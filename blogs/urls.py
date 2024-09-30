from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.apps import BlogConfig
from blogs.views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BlogListView,
    BlogUpdateView,
    blog_is_publication,
)

app_name = BlogConfig.name

urlpatterns = [
    path("create/", BlogCreateView.as_view(), name="create"),
    path("", BlogListView.as_view(), name="list"),
    path("view/<int:pk>/", cache_page(60)(BlogDetailView.as_view()), name="view"),
    path("update/<int:pk>/", BlogUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", BlogDeleteView.as_view(), name="delete"),
    path("activity/<int:pk>/", blog_is_publication, name="blog_is_publication"),
]
