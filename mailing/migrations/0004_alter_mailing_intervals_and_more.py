# Generated by Django 4.2.2 on 2024-09-24 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0003_mailing_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="intervals",
            field=models.CharField(
                blank=True,
                choices=[
                    ("daily", "Ежедневно"),
                    ("weekly", "Еженедельно"),
                    ("monthly", "Ежемесячно"),
                ],
                max_length=50,
                null=True,
                verbose_name="Периодичность",
            ),
        ),
        migrations.AlterField(
            model_name="mailinglog",
            name="status_mailing",
            field=models.CharField(
                choices=[("success", "success"), ("fail", "fail")],
                default="success",
                verbose_name="Статус попытки",
            ),
        ),
    ]
