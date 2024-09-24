from django.db import models
from django.utils import timezone

NULLABLE = {"blank": True, "null": True}

PERIODICITY_CHOICES = [
    ("daily", "Ежедневно"),
    ("weekly", "Еженедельно"),
    ("monthly", "Ежемесячно"),
]

STATUS_CHOICES = [
    ("created", "Создана"),
    ("started", "Запущена"),
    ("completed", "Завершена"),
]


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name="Клиент")
    email = models.EmailField(verbose_name="Email", unique=True)
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("email",)

    def __str__(self):
        return f"Клиент {self.email}({self.name})"


class Message(models.Model):
    message_theme = models.CharField(
        max_length=150,
        help_text="Введите тему сообщения",
        verbose_name="Тема сообщения",
    )
    message_body = models.TextField(
        help_text="Введите текст сообщения", verbose_name="Содержание"
    )

    def __str__(self):
        return self.message_theme

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("message_theme",)


class Mailing(models.Model):
    first_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата и время начала рассылки",
        help_text="Введите дату и время начала рассылки",
        **NULLABLE,
    )
    next_date = models.DateTimeField(
        verbose_name="Дата и время следующей отправки рассылки", **NULLABLE
    )
    last_date = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        help_text="Введите дату и время окончания рассылки",
        **NULLABLE,
    )
    intervals = models.CharField(
        max_length=10,
        choices=PERIODICITY_CHOICES,
        verbose_name="Периодичность",
        **NULLABLE,
    )
    mailing_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="created",
        verbose_name="Статус рассылки",
    )
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )
    clients = models.ManyToManyField(
        Client, verbose_name="Клиенты", related_name="mailings"
    )

    def __str__(self):
        return f'Рассылка "{self.message}"'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("intervals",)


class MailingLog(models.Model):
    last_mailing = models.DateTimeField(
        verbose_name="Дата и время последней попытки", **NULLABLE
    )
    status_mailing = models.BooleanField(verbose_name="Статус попытки", default=True)
    mail_response = models.TextField(verbose_name="Ответ почтового сервера", **NULLABLE)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="logs"
    )

    def __str__(self):
        return f'Попытка рассылки "{self.mailing.pk}"'

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ("status_mailing",)
