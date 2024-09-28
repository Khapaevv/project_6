from django.core.management import BaseCommand

from mailing.cron import daily_mailings


class Command(BaseCommand):
    """Команда запуска рассылок"""

    def handle(self, *args, **options):
        daily_mailings()
        print("run mailing")
