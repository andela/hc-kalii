import json

from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase
from mock import patch


@override_settings(PUSHBULLET_CLIENT_ID="t1", PUSHBULLET_CLIENT_SECRET="s1")
class AddPushbulletTestCase(BaseTestCase):
    def test_it_shows_instructions(self):
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/integrations/add_twitter/")
        self.assertContains(r, "http://gettwitterid.com/", status_code=200)

    def test_it_adds_twitter(self):
        url = "/integrations/add/"
        form = {"kind": "twitter", "value": 2547142605350}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1
