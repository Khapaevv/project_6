from django.contrib import admin
from mailing.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_filter = ('email',)
    verbose_name = 'Клиенты'

