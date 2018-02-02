from hc.test import BaseTestCase
from hc.api.models import Check
from django.contrib.auth.models import User

class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        bob = User.objects.get(email="bob@example.org")
        c = Check(user=self.alice, name="This belongs to Alice",
                  member_access_allowed=True, member_access_id=bob.id)
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        team_alice = self.client.get(url, follow=True)

        ### Assert the contents of r
        self.assertContains(team_alice, "This belongs to Alice")  # Alice's check should appear in team view

    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        forbidden = self.client.get(url)
        ### Assert the expected error code
        self.assertEqual(403, forbidden.status_code)  # should return 403 forbidden for Charlie

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        ### Assert the expected error code
        self.assertEqual(200, r.status_code)


