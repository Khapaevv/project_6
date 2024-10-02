from django.core.cache import cache

from config import settings
from mailing.models import Client, Mailing


def get_cached_objects(cache_key, model_cls):
    """Универсальная функция для получения объектов из кэша или базы данных."""
    if settings.CACHE_ENABLED:
        cached_objects = cache.get(cache_key)
        if cached_objects is None:
            objects = model_cls.objects.all()
            cache.set(cache_key, objects)
        else:
            objects = cached_objects
    else:
        objects = model_cls.objects.all()

    return objects


# Get mailing list
mailing_list = get_cached_objects("mailing_list", Mailing)

# Get client list
client_list = get_cached_objects("client_list", Client)
