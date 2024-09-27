from django.core.management import BaseCommand
from mailing.services import send_mailing


class Command(BaseCommand):
    """Команда запуска рассылок"""
    def handle(self, *args, **options):
        send_mailing()