from django.core.cache import cache

from blogs.models import Blog
from config.settings import CACHE_ENABLED


def get_blogs_from_cache():
    if not CACHE_ENABLED:
        return Blog.objects.filter(is_published=True)

    key = "published_blog_list"
    blogs = cache.get(key)
    if blogs is not None:
        return blogs

    blogs = Blog.objects.filter(is_published=True)
    cache.set(key, blogs, timeout=60 * 15)
    return blogs
