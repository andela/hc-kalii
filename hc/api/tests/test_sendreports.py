from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from mock import patch

from hc.accounts.models import Profile
from hc.api.management.commands.sendreports import Command
from hc.api.models import Check
from hc.test import BaseTestCase

class SendReportsTestCase(BaseTestCase):
    """ Test sending of reports using API Command """

    @patch("hc.api.management.commands.sendreports.Command.handle_one_run")
    def test_it_handles_few(self, mock):
        """ Test that API handles sending of few reports """
        date_joined = timezone.now() - timedelta(days=2)
        usernames = ["testuser%d" % d for d in range(0, 5)]

        for username in usernames:
            user = User(username=username, email=username + "@example.org", date_joined=date_joined)
            user.set_password("password")
            user.save()
            profile = Profile(user=user, api_key="def")
            profile.team_access_allowed = True
            profile.save()
            check = Check(user=user, name="Cron I", status="up")
            check.save()
            self.client.get("/ping/%s/" % check.code)

        result = Command().handle_many()
        self.assertTrue(result)

        handled_users = []
        for args, kwargs in mock.call_args_list:
            handled_users.append(args[0].user.username)

        assert set(usernames) == set(handled_users)
