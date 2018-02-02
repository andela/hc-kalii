from hc.test import BaseTestCase
from hc.front.models import Category, Blog_post

class DeleteBlogTest(BaseTestCase):
    def setUp(self):
        super(DeleteBlogTest, self).setUp()
        self.category = Category(name="test category")
        self.category.save()
        self.blog = Blog_post(title='title', content='content', category=self.category)
        self.blog.save()
        

    def test_blog_is_deleted(self):
        url = "/blog/delete_blog/1"
        # data = {'title': ['sajdgjs'], 'content': ['gjsagjdgaj'],'category': ['1']}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(url)

        self.assertEquals(r.status_code, 302)
        assert Blog_post.objects.count() == 0