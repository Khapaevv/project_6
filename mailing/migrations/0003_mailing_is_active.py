# Generated by Django 4.2.2 on 2024-09-24 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_mailing_message_alter_client_options_mailinglog_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailing",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
