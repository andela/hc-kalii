from django.contrib.auth.models import User
from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_access_works(self):
        check = Check(user=self.alice, name="Team check")
        check.save()
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            dashboard = self.client.get("/checks/")
            self.assertContains(dashboard, "Team check")
        self.client.login(username="charlie@example.org", password="password")
        dashboard = self.client.get("/checks/")
        self.assertNotContains(dashboard, "Team check")