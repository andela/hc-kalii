import re

from django.core import mail

from hc.test import BaseTestCase
from hc.accounts.models import Member, Profile, User
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):

    def _invite_member(self, email):
        """
        This is helper method invites a new team member
        """
        form = {"invite_team_member": "1", "email": email, "check":"Cron A"}
        response = self.client.post("/accounts/profile/", form)
        self.assertEqual(response.status_code, 200)

    def _get_member(self, email):
        """
        This helper method gets a specific member from a team
        """
        user = User.objects.get(email=email)
        return Member.objects.filter(team=self.alice.profile, user=user).first()

    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        ### Assert that the token is set
        self.assertTrue(token)
        ### Assert that the email was sent and check email content

    def test_it_sends_default_reports(self):
        ### Test if default reports are sent to user via email
        check = Check(name="Test Check", user=self.alice)
        check.save()
        self.alice.profile.send_report()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Monthly Report')
        self.assertIn('This is a monthly report sent by healthchecks.io', str(mail.outbox[0].body))

    def test_it_sends_daily_reports(self):
        ### Test that daily reports are sent to user via email
        self.client.login(username="alice@example.org", password="password")
        form = {"update_reports_allowed": 1, "reports_allowed": True, "report_period": 1}
        res = self.client.post("/accounts/profile/", form)
        self.assertEqual(res.status_code, 302)
        self.alice.profile.refresh_from_db()
        check = Check(name="Cron A", user=self.alice)
        check.save()
        self.alice.profile.send_report()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Daily Report')
        self.assertIn('This is a daily report sent by healthchecks.io', str(mail.outbox[0].body))

    def test_it_sends_weekly_reports(self):
        ### Test that weekly reports are sent to user via email
        self.client.login(username="alice@example.org", password="password")
        form = {"update_reports_allowed": 1, "reports_allowed": True, "report_period": 7}
        res = self.client.post("/accounts/profile/", form)
        self.assertEqual(res.status_code, 302)
        self.alice.profile.refresh_from_db()
        check = Check(name="Cron A", user=self.alice)
        check.save()
        self.alice.profile.send_report()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Weekly Report')
        self.assertIn('This is a weekly report sent by healthchecks.io', str(mail.outbox[0].body))

    def test_it_sends_monthly_reports(self):
        ### Test if monthly reports are sent to user via email
        self.client.login(username="alice@example.org", password="password")
        form = {"update_reports_allowed": 1, "reports_allowed": True, "report_period": 30}
        res = self.client.post("/accounts/profile/", form)
        self.assertEqual(res.status_code, 302)
        self.alice.profile.refresh_from_db()
        check = Check(name="Cron A", user=self.alice)
        check.save()
        self.alice.profile.send_report()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Monthly Report')
        self.assertIn('This is a monthly report sent by healthchecks.io', str(mail.outbox[0].body))

    def test_user_reports_on_dashboard(self):
        ### Test if user can see reports on dashboard
        check = Check(name="Cron A", user=self.alice)
        check.save()
        self.client.login(username="alice@example.org", password="password")
        res = self.client.get("/accounts/reports/")
        self.assertEqual(res.status_code, 200)

    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")
        check = Check(name="Cron A", user=self.alice)
        check.save()

        form = {"invite_team_member": "1", "email": "frank@example.org", "check": "Cron A"}
        invitation = self.client.post("/accounts/profile/", form)
        assert invitation.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        ### Assert the existence of the member emails
        # assert member email exists with existing team members
        self.assertTrue("bob@example.org" in member_emails)
        self.assertTrue("frank@example.org" in member_emails)

        ###Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, 'You have been invited to join alice@example.org on healthchecks.io')
        self.assertIn('please open the link below:', str(
            mail.outbox[0].body),)  # assert email body

    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        invitation = self.client.post("/accounts/profile/", form)
        assert invitation.status_code == 403

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        team_name = self.client.post("/accounts/profile/", form)
        assert team_name.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        team_name = self.client.post("/accounts/profile/", form)
        assert team_name.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        badge = self.client.get("/accounts/profile/")
        self.assertContains(badge, "foo.svg")
        self.assertContains(badge, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(badge, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(badge, "bobs-tag.svg")

    ### Test it creates and revokes API key

    def test_user_can_revoke_api_key(self):
        """
        User should be able to revoke an api
        :return:  True
        """
        self.client.login(username="alice@example.org", password="password")
        api_key = self.alice.profile.api_key
        self.assertEqual(api_key, 'abc')  # Assert that api key created

        form = {"revoke_api_key": ""}
        self.client.post("/accounts/profile/", form)  # revoke the api key
        self.alice.profile.refresh_from_db()
        api_key = self.alice.profile.api_key
        self.assertEqual("", api_key)

    def test_user_can_create_api_key(self):
        """
        User should be able to create an api after revoking it
        :return: True
        """
        self.client.login(username="alice@example.org", password="password")
        api_key = self.alice.profile.api_key
        self.assertEqual(api_key, 'abc')  # Assert that api key created

        form = {"revoke_api_key": ""}
        # Try and revoke the api key
        self.client.post("/accounts/profile/", form)
        self.alice.profile.refresh_from_db()
        api_key = self.alice.profile.api_key  # Should return None
        self.assertEqual("", api_key)

        #// CREATE AN API KEY AFTER REVOKING IT

        form = {"create_api_key": ""}
        self.client.post("/accounts/profile/", form)
        self.alice.profile.refresh_from_db()

        api_key = self.alice.profile.api_key  # should return a new api key
        assert api_key

    def test_adding_team_member_with_lowest_priority(self):
        """
        Ensure that a new team member is added leading the priority
        to reduce in turn
        """
        self.client.login(username="alice@example.org", password="password")
        check = Check(name="Cron A", user=self.alice)
        check.save()
        self._invite_member("glassman@example.org")
        user = User.objects.filter(email="glassman@example.org")

        member = self._get_member("glassman@example.org")
        self.assertTrue(member.priority, "LOW")

    def test_update_priority(self):
        """
        Ensure that the team member priority can be updated
        """
        self.client.login(username="alice@example.org", password="password")
        check = Check(name="Cron A", user=self.alice)
        check.save()
        self._invite_member("glassman@example.com")
        member = self._get_member("glassman@example.com")
        self.assertTrue(member.priority, "LOW")

        form = {"update_priority": "1", "email": "glassman@example.com", "check": "Cron A"}
        response = self.client.post("/accounts/profile/", form)
        self.assertEqual(response.status_code, 200)

        member = self._get_member("glassman@example.com")
        self.assertTrue(member.priority, "HIGH")




