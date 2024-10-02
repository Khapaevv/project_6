from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):

    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    slug = models.CharField(
        max_length=150,
        verbose_name="Иденфикатор",
        null=True,
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите содержимое",
    )
    image = models.ImageField(
        upload_to="products/image",
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        **NULLABLE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )
    count_views = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title
