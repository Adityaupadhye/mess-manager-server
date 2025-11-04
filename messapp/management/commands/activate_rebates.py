from django.core.management.base import BaseCommand
from django.utils import timezone
from messapp.models import MessRebates
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates MessRebates status to expired if end_date has passed and status is active'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        logger.info(f'today is {today}')
        # filter records for inactive status and make then active based on the date condition
        inactive_rebates = MessRebates.objects.filter(status="inactive", end_date__gte=today, start_date__lte=today)
        count = inactive_rebates.update(status="active")

        logger.info(f'{count} records updated to active status.')
        self.stdout.write(f'{count} records updated to active status.')
