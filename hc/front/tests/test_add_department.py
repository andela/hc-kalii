from hc.api.models import Department
from hc.test import BaseTestCase


class AddDepartmentTestCase(BaseTestCase):
    """ Test for new department creation """

    def test_it_works(self):
        """ Test that new department can be created using URL """
        self.client.login(username="alice@example.org", password="password")

        form = {"name": "Marketing"}
        response = self.client.post("/departments/add/", form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Department.objects.filter(user=self.alice).count(), 1)
