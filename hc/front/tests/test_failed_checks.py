from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta
from django.utils import timezone


class MyFailedChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyFailedChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Failing checks")
        self.check.last_ping = timezone.now() - timedelta(days=3)
        self.check.status = "up"
        self.check.save()

    def test_unresolved_checks_show_in_endpoint_failed_checks(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            unresolved_checks = self.client.get("/failed_checks/")
            self.assertContains(unresolved_checks, "Failing checks", status_code=200)