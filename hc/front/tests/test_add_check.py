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
        url="/checks/add/"
        #Bob logs in and adds a new check. Bob is on the team
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)

        # Charlie logins and attempts to add a new check, charlie has no team access
        self.client.login(username="charlie@example.org", password="password")
        self.client.post(url)

        user_alice = User.objects.get(email="alice@example.org")
        #Alice can access the team's check since she is also on the team
        assert Check.objects.filter(user=user_alice).count() == 1
