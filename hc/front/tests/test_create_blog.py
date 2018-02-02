from hc.test import BaseTestCase
from hc.front.models import Category, Blog_post

class CreateBlogTest(BaseTestCase):
    def setUp(self):
        super(CreateBlogTest, self).setUp()
        self.category = Category(name="test category")
        self.category.save()

    def test_blog_is_created(self):
        url = "/blog/create_blog"
        data = {'title': ['sajdgjs'], 'content': ['gjsagjdgaj'],'category': ['1']}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data)

        self.assertEquals(r.status_code, 302)
        assert Blog_post.objects.count() == 1