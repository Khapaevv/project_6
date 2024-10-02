from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )
    phone = models.CharField(
        max_length=13,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        **NULLABLE
    )
    country = models.CharField(
        max_length=50, verbose_name="Страна", help_text="Введите страну", **NULLABLE
    )

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("set_active_user", "Can active user"),
            ("set_viewing_user", "Can viewing user"),
        ]

    def __str__(self):
        return self.email
