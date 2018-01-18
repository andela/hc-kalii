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
    def test_login_redirects_already_logged_in(self):
        """Tests if user is already logged in. Visiting the token link again
        should return him to his dashboard
        :returns: link should be valid as long as user is logged in: True
        """
        login = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(login, "/checks/")

        already_logged = self.client.get("/") # Test redirect to dashboard
        self.assertRedirects(already_logged, "/checks/")

        login_again = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(login_again, "/checks/")

    ### Login with a bad token and check that it redirects
    def test_login_InvalidToken_ShouldNotAccept(self):
        """
        Test if user will be logged in with provided that he gave a bad token
        :return: redirects back to login page
        """
        bad_login_token = self.client.post("/accounts/check_token/alice/some-radom-token/") #  post with bad token
        self.assertRedirects(bad_login_token, "/accounts/login/", status_code=302)


    ### Any other tests?

    def test_login_OneTimeToken_ShouldNotAcceptOnNextLogin(self):
        """
        A one time login should not be accepted on next login
        :return: Return redirect back to login
        """
        self.client.post("/accounts/check_token/alice/secret-token/")  # login


        self.client.get("/accounts/logout/")  #logout

        login = self.client.post("/accounts/check_token/alice/secret-token/")  # Previous used token
        self.assertRedirects(login, "/accounts/login/")  # Refuse and Redirect back to login


