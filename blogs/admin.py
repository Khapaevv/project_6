from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('created_at', 'is_published')
    search_fields = ('name', 'descriptions')
    verbose_name = 'Блог'