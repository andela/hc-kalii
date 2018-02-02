from hc.api.models import Department
from hc.test import BaseTestCase


class EditDepartmentTestCase(BaseTestCase):
    """ Test for editing of department """

    def setUp(self):
        super(EditDepartmentTestCase, self).setUp()
        Department.objects.create(user=self.alice, name="Marketing")
        self.department = Department.objects.get(name="Marketing")
        self.url = ("/departments/edit/%s/" % str(self.department.id))

    def test_edit_department_url_works(self):
        """ Test that edit department page URL can be accessed """
        self.client.login(username="alice@example.org", password="password")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_department_can_be_edited(self):
        """ Test that department can be edited """
        self.client.login(username="alice@example.org", password="password")

        form = {"name": "Operations"}
        response = self.client.post(self.url, form)
        self.assertEqual(response.status_code, 302)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, "Operations")
