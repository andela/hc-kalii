import json

from hc.api.models import Channel, Check, Department
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)

            ### Assert that the expected error is the response error
            self.assertEqual(r.json()['error'], expected_error)

        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        ### Assert the expected last_ping and n_pings values

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)
        self.assertEqual(check.last_ping, None)
        self.assertEqual(check.n_pings, 0)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        r = self.post({"api_key": "abc"})
        self.assertEqual(r.status_code, 201)

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response
        r = self.post({}, expected_error="wrong api_key")
        self.assertEqual(r.status_code, 400)

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        r = self.client.post(self.URL, {"api_key": "abc"}, content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['error'], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    def test_it_rejects_small_timeout(self):
        ### Test for small timeout
        self.post({"api_key": "abc", "timeout": 40},
                  expected_error="timeout is too small")

    def test_it_rejects_large_timeout(self):
        ### Test for large timeout
        self.post({"api_key": "abc", "timeout": 90077567846},
                  expected_error="timeout is too large")

    def test_it_assigns_channels(self):
        ### Test for the assignment of channels
        channel = Channel(user=self.alice)
        channel.kind = "slack"
        channel.save()
        self.post({
            "api_key": "abc",
            "name": "Foo",
            'channels': "*"
        })

        check = Check.objects.get(name='Foo')
        self.assertTrue(check.channel_set.filter(kind='slack').exists())

    def test_can_be_assigned_department(self):
        """ Test for assignment of departments """
        department = Department(user=self.alice, name="Info Tech")
        department.save()
        response = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "department_id": 1
        })

        self.assertEqual(response.status_code, 201)
        check = Check.objects.get(name='Foo')
        self.assertEqual(check.department.name, "Info Tech")
