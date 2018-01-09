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
    def test_it_redirects_already_logged_in_provided_we_do_a_request_with_the_token_again(self):
        """Tests if user is already logged in. Visiting the token link again
        should return him to his dashboard
        :returns: link should be valid as long as user is logged in: True
        """
        login = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(login, "/checks/")

        already_logged = self.client.get("/") #  check to see if user will be redirected to dashboard
        self.assertRedirects(already_logged, "/checks/")

        login_again = self.client.get("/accounts/check_token/alice/secret-token/") # the same token should work again
        self.assertRedirects(login_again, "/checks/")

    ### Login with a bad token and check that it redirects
    def test_when_a_user_login_with_bad_token(self):
        """
        Test if user will be logged in with provided that he gave a bad token
        :return: redirects back to login page
        """
        bad_login_token = self.client.post("/accounts/check_token/alice/some-radom-token/") #  post with bad token
        self.assertRedirects(bad_login_token, "/accounts/login/", status_code=302)


    ### Any other tests?

    def test_for_token_should_not_be_valid_once_the_user_logs_out(self):
        """
        Test if a token is reusable after logout
        :return: authentication should refuse login with previous token
        """
        login = self.client.post("/accounts/check_token/alice/secret-token/")  # login the user
        self.assertRedirects(login, "/checks/")

        logout = self.client.get("/accounts/logout/")  #logout user
        self.assertRedirects(logout, "/", status_code=302)


