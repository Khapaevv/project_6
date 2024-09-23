from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Клиент')
    email = models.EmailField(verbose_name='Email', unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'Клиент {self.email}({self.name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
