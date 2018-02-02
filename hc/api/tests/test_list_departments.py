import json

from hc.api.models import Department
from hc.test import BaseTestCase


class ListDepartmentsTestCase(BaseTestCase):
    """ Test for listing of departments """

    def setUp(self):
        super(ListDepartmentsTestCase, self).setUp()

        self.department1 = Department(user=self.alice, name="Operations")
        self.department1.save()

        self.department2 = Department(user=self.alice, name="Marketing")
        self.department2.save()

    def test_it_works(self):
        """ Test that departments created can be returned by API endpoint """
        response = self.client.get("/api/v1/departments/", HTTP_X_API_KEY="abc")
        self.assertEqual(response.status_code, 200)
        doc = response.json()
        self.assertTrue("departments" in doc)
        departments = {department["name"]: department for department in doc["departments"]}
        self.assertTrue(departments['Operations'])
        self.assertTrue(departments['Marketing'])
