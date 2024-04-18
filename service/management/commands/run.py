import datetime
from django.core.management.base import BaseCommand
class Command(BaseCommand):

    def handle(self, *args, **options):
        current_date = datetime.datetime.now()

        srp_start = current_date.strftime('%Y-%m-%d %H:%M:%S')
        date_object_start = datetime.datetime.strptime(srp_start, '%Y-%m-%d %H:%M:%S')
        print(current_date)