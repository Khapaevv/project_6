from django.contrib import admin

from mailing.models import Client, Mailing, MailingLog, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    list_filter = ("email",)
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "message_theme", "message_body")
    list_filter = ("message_theme",)
    search_fields = ("message_theme",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "intervals", "mailing_status", "is_active")
    list_filter = ("clients", "intervals", "mailing_status")
    search_fields = ("clients", "intervals", "mailing_status")


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ("id", "last_mailing", "status_mailing", "mail_response", "mailing")
    list_filter = ("last_mailing", "status_mailing")
    search_fields = ("status_mailing",)
