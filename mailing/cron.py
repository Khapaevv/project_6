from datetime import timezone
from smtplib import SMTPException

from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, MailingLog


def send_mailing():
    current_time = timezone.localtime(timezone.now())

    mailings = Mailing.objects.filter(is_active=True)

    if mailings is None:
        print("Нет рассылок готовых к отправке")

    else:
        for mailing in mailings:
            if mailing.first_date <= current_time < mailing.last_date:
                mailing.mailing_status = Mailing.STARTED
                mailing.save()
                try:
                    result = send_mail(
                        subject=mailing.message.message_theme,
                        message=mailing.message.message_body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.client.filter(is_active=True)]
                    )
                    log = MailingLog.objects.create(
                        last_mailing=mailing.first_date,
                        status_mailing=result,
                        response_server='SUCCESS',
                        mailing=mailing
                    )
                    log.save()
                    return log
                except SMTPException as error:
                    log = MailingLog.objects.create(
                        last_mailing=mailing.first_date,
                        status_mailing=False,
                        response_server=error,
                        mailing_list=mailing,
                    )
                    log.save()
                    return log
            else:
                mailing.status = Mailing.COMPLETED
                mailing.save()


def daily_mailings():
    mailings = Mailing.objects.filter(intervals="Раз в день")
    print(mailings)
    if mailings.exists():
        send_mailing()



def weekly_mailings():
    mailings = Mailing.objects.filter(intervals="Раз в неделю", mailing_status="Запущена")
    if mailings.exists():
        send_mailing()


def monthly_mailings():
    mailings = Mailing.objects.filter(intervals="Раз в месяц", mailing_status="Запущена")
    if mailings.exists():
        send_mailing()