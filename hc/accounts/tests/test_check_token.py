from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_it_redirects_already_logged_in(self):
        """Tests if user is already logged in. it redirects him back to login
        """
        login = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(login, "/checks/")

        Already_logged = self.client.get("/") #  check to see if user will be redirected to dashboard
        self.assertRedirects(Already_logged, "/checks/")


    ### Login with a bad token and check that it redirects

    ### Any other tests?
