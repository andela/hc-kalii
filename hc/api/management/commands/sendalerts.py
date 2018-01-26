import logging
import time

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from hc.api.models import Check
from hc.accounts.models import Member
from hc.api.models import Channel
executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends UP/DOWN email alerts'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down = query.filter(alert_after__lt=now, status="up")
        going_up = query.filter(alert_after__gt=now, status="down")
        nagging_on = query.filter(
            nag_after__lt=now, nag_status=True, status="down")
        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down.iterator()) + \
            list(going_up.iterator()) + list(nagging_on.iterator())
        if not checks:
            return False

        futures = [executor.submit(self.handle_one, check) for check in checks]
        for future in futures:
            future.result()

        return True

    def handle_one(self, check):
        """ Send an alert for a single check.

        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.

        """

        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        check.status = check.get_status()
        check.save()
        if check.status == "down":
            self.notify_members(check)
            check.nag_after = (timezone.now() + check.interval)
            check.nag_status = True
            check.save()

        self.send_alert(check)
        connection.close()
        return True

    def send_alert(self, check):
        """
        This helper method  notifies a user
        """
        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))
        errors = check.send_alert()
        for ch, error in errors:
            self.stdout.write("ERROR: %s %s %s\n" %
                              (ch.kind, ch.value, error))

        connection.close()
        return True

    def handle(self, *args, **options):
        self.stdout.write("sendalerts is now running")

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

    def notify_members(self, check):
        """
        This method notifies members in the team
        """
        members = Member.objects.filter(
            team=check.user.profile, priority="HIGH").all()
        for member in members:
            channel = Channel.objects.filter(value=member.user.email).first()
            error = channel.notify(check)
            if error not in ("", "no-op"):
                print("%s, %s" % (channel, error))
