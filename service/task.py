from service.services import send_newsletter
from service.models import MailingSettings


def daily_task():
    mailings = MailingSettings.objects.filter(periodicity='Раз в день', status='Запущена')
    if mailings.exists():
        for mailing in mailings:
            send_newsletter(mailing)


def weekly_task():
    mailings = MailingSettings.objects.filter(periodicity='Раз в неделю', status='Запущена')
    if mailings.exists():
        for mailing in mailings:
            send_newsletter(mailing)


def monthly_task():
    mailings = MailingSettings.objects.filter(periodicity='Раз в месяц', status='Запущена')
    if mailings.exists():
        for mailing in mailings:
            send_newsletter(mailing)
