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
        # Filter records where status is "active" and end_date is before today
        expired_rebates = MessRebates.objects.filter(status="active", end_date__lt=today)
        count = expired_rebates.update(status="expired")

        logger.info(f'{count} records updated to expired status.')
        self.stdout.write(f'{count} records updated to expired status.')
