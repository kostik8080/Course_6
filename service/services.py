from datetime import timedelta
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from service.models import MailingSettings, Log

def send_newsletter(mailing):
    now = timezone.localtime(timezone.now())
    recipient_list = MailingSettings.objects.all()
    from_email = settings.EMAIL_HOST_USER
    if mailing.start_time > mailing.end_time:
        mailing.status = 'Завершена'
        mailing.save()
    if mailing.start_time <= now <= mailing.end_time:
        for recipient in recipient_list:
            recipient.status = 'Запущена'
            recipient.save()
            client_emails = [client.email for client in recipient.clients.all()]
            subject = recipient.mailing_list.title
            message = recipient.mailing_list.text

            for client_email in client_emails:
                try:
                    send_mail(subject, message, from_email, [client_email], fail_silently=False)
                    now = timezone.localtime(timezone.now())
                    log = Log.objects.create(time=now, status=True, server_response='Yes', mailing_list=recipient)
                    if recipient.start_time < recipient.end_time:

                        if recipient.periodicity == 'Раз в день':

                            recipient.start_time += timezone.timedelta(days=1)
                            recipient.status = 'Создана'
                            recipient.save()

                        elif recipient.periodicity == 'Раз в неделю':
                            recipient.start_time += timezone.timedelta(days=7)
                            recipient.status = 'Создана'
                            recipient.save()
                        elif recipient.periodicity == 'Раз в месяц':
                            recipient.start_time += timezone.timedelta(days=30)
                            recipient.status = 'Создана'
                            recipient.save()

                    elif recipient.start_time >= recipient.end_time:
                        recipient.start_time = recipient.end_time
                        recipient.status = 'Завершена'
                        recipient.save()
                except SMTPException as error:
                    now = timezone.localtime(timezone.now())
                    log = Log.objects.create(time=now, status=False, server_response='No', mailing_list=recipient)
                    recipient.status = 'Создана'
                    recipient.save()

