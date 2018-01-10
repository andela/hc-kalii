from django.test.utils import override_settings
from django.contrib.auth.models import User
from hc.api.models import Channel, Ping
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """
        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)
        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ## Test that the team access works
    def test_team_access_works(self):
        url = "/integrations/add/"
        form = {"kind": "email"}
        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, form)
        user_alice = User.objects.get(email="alice@example.org")
        user_charlie = User.objects.get(email="charlie@example.org")
        # Alice created team and has team access
        self.assertEquals(Channel.objects.filter(user=user_alice).count(), 1)
        # Charlie is not part of the team so he should have no Channel
        self.assertEquals(Channel.objects.filter(user=user_charlie).count(), 0)

    ### Test that bad kinds don't work
    def test_bad_kinds_dont_work(self):
        url = "/integrations/add/"
        form = {"kind": "bad_kind", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        self.assertEquals(response.status_code, 400)
