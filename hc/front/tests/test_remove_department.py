from hc.api.models import Department
from hc.test import BaseTestCase


class DeleteDepartmentTestCase(BaseTestCase):
    """ Test for removal of departments """

    def setUp(self):
        super(DeleteDepartmentTestCase, self).setUp()
        Department.objects.create(user=self.alice, name="Marketing")
        self.department = Department.objects.get(name="Marketing")
        self.url = ("/departments/remove/%s/" % str(self.department.id))

    def test_department_can_be_removed(self):
        """ Test that department can be removed """
        self.client.login(username="alice@example.org", password="password")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
