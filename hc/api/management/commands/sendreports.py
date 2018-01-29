import time
import logging
from datetime import timedelta

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from hc.accounts.models import Profile
from hc.api.models import Check

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)

def num_pinged_checks(profile):
    """ Check for number of currently pinged checks """
    checks = Check.objects.filter(user_id=profile.user.id,)
    checks = checks.filter(last_ping__isnull=False)
    return checks.count()

class Command(BaseCommand):
    help = 'Send due reports'
    tmpl = "Sending report to %s"

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            dest='loop',
            default=False,
            help='Keep running indefinitely in a 300 second wait loop',
        )

    def handle_many(self):
        """ Send reports for many users simultaneously. """
        now = timezone.now()
        day_before = now - timedelta(days=1)
        report_due = Q(next_report_date__lt=now)
        report_not_scheduled = Q(next_report_date__isnull=True)

        reports = Profile.objects.filter(report_due | report_not_scheduled)
        reports = reports.filter(reports_allowed=True)
        reports = reports.filter(user__date_joined__lt=day_before)

        if not reports:
            return False

        futures = [executor.submit(self.handle_one_run, profile) for profile in reports]
        for future in futures:
            future.result()

        return True

    def handle_one_run(self, profile):
        """ Handle sending on one report. """
        if num_pinged_checks(profile) > 0:
            self.stdout.write(self.tmpl % profile.user.email)
            profile.send_report()

        return True

    def handle(self, *args, **options):
        """" Handle sending of reports continuously. """
        self.stdout.write("sendreports is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)
