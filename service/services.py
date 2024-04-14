from smtplib import SMTPException

from django.conf import settings
from django.contrib.sites import requests
from django.core.mail import send_mail
from django.utils import timezone

from service.models import Client, MailingSettings, Message, Log


def send_newsletter(mailing):
    now = timezone.localtime(timezone.now())
    if mailing.start_time <= now <= mailing.end_time:
        recipient_list = MailingSettings.objects.all()
        from_email = settings.EMAIL_HOST_USER

        for recipient in recipient_list:
            client_emails = [client.email for client in recipient.clients.all()]
            subject = recipient.mailing_list.title
            message = recipient.mailing_list.text
            for client_email in client_emails:
                try:
                    result = send_mail(subject, message, from_email, [client_email], fail_silently=False)
                    now = timezone.localtime(timezone.now())
                    log = Log.objects.create(time=now, status=True, server_response='Yes',
                                         mailing_list=mailing)

                except SMTPException as error:
                    now = timezone.localtime(timezone.now())
                    log = Log.objects.create(time=now, status=False, server_response='No',
                                         mailing_list=mailing)




