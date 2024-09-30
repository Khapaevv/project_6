from django.urls import include, path

from mailing.apps import MailingConfig
from mailing.views import (
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    ClientListView,
    ClientUpdateView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingUpdateView,
    MainPageView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    get_mailinglog_view,
)

app_name = MailingConfig.name


urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client_create/", ClientCreateView.as_view(), name="client_create"),
    path("client_update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("message_list", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailings_list", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing_update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("logs_list/", get_mailinglog_view, name="logs_list"),
]
