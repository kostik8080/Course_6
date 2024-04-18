import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from service.services import send_newsletter
from service.task import daily_task, weekly_task, monthly_task

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # send_newsletter()
        #daily_task()
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            daily_task,
            trigger=CronTrigger(minute='*/1'),
            id="daily_job",
            max_instances=1,
            replace_existing=True,
        )
        # logger.info("Added 'daily job'.")
        #
        # scheduler.add_job(
        #     weekly_task,
        #     trigger=CronTrigger(day_of_week='*/1'),
        #     id="weekly_job",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added  'weekly job'.")
        # scheduler.add_job(
        #     monthly_task,
        #     trigger=CronTrigger(day='*/30'),
        #     id="monthly_job",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added 'monthly job'.")
        # scheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week='mon',
        #         hour=0,
        #         minute=00,
        #     ),
        #     id="delete_old_job_executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added weekly job: 'delete_old_job_executions'.")
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
