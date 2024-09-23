from django.urls import path, include
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('',),
]
