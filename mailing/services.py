from django.core.cache import cache

from config import settings
from mailing.models import Client, Mailing


def get_cached_main():
    if settings.CACHE_ENABLED:
        key = "mailing_list"
        mailing_list = cache.get(key)
        if mailing_list is None:
            mailing_list = Mailing.objects.all()
            cache.set(key, mailing_list)
    else:
        mailing_list = Mailing.objects.all()

    return mailing_list


def get_cached_client():
    if settings.CACHE_ENABLED:
        key = "client_list"
        client_list = cache.get(key)
        if client_list is None:
            client_list = Client.objects.all()
            cache.set(key, client_list)
    else:
        client_list = Client.objects.all()

    return client_list


