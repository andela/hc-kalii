from hc.test import BaseTestCase
from hc.front.models import Category

class CreateCategoryTest(BaseTestCase):

    # def setUp(self):
    #     super(CreateCategoryTest, self).setUp()
    #     self.Category = Channel(user=self.alice, kind="email")
    #     self.channel.value = "alice@example.org"
    #     self.channel.save()

    # def test_it_works(self):
    #     url = "/integrations/%s/remove/" % self.channel.code

    #     self.client.login(username="alice@example.org", password="password")
    #     r = self.client.post(url)
    #     self.assertRedirects(r, "/integrations/")

    #     assert Channel.objects.count() == 0

    def test_category_is_created(self):
        url = "/blog/create_blog"
        data = {'name' :['fgajfgjagd']}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data)

        self.assertEquals(r.status_code, 200)
        assert Category.objects.count() == 1