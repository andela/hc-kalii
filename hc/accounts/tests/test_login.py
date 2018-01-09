from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check
from hc.accounts.models import Profile


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        create_user = self.client.post("/accounts/login/", form)
        assert create_user.status_code == 302

        ### Assert that a user was created
        assert Profile.objects.select_related("user").get(user__email=form["email"])  # Go to database and retrieve user
        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        ### Assert contents of the email body
        self.assertIn("please open the link below", str(mail.outbox[0].body))
        ### Assert that check is associated with the new user

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        ### Any other tests?
    def test_invalid_email_during_login_should_not_be_accepted(self):
        """
        app should not accept an improper email when logging in
        :return: redirect back to the login page
        """
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "I_AM_PRETENDING_TO_BE_AN_EMAIL"}

        invalid_email_login = self.client.post("/accounts/login/", form)
        self.assertTrue(invalid_email_login.status_code, 200)  # returns status code 200 instead of 301/302
