import json

from hc.test import BaseTestCase


class CreateDepartmentTestCase(BaseTestCase):
    """ Test for new department creation """

    URL = "/api/v1/departments/"

    def test_it_works(self):
        """ Test that new department can be created using the API endpoint """
        data = {"api_key": "abc", "name": "Info Tech"}
        response = self.client.post(self.URL, json.dumps(data), \
                content_type="application/json")
        self.assertEqual(response.status_code, 201)
        doc = response.json()
        self.assertEqual(doc["name"], "Info Tech")
