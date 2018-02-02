from hc.test import BaseTestCase
from hc.front.models import Category, Blog_post

class UpdateBlogTest(BaseTestCase):
    def setUp(self):
        super(UpdateBlogTest, self).setUp()
        self.category = Category(name="test category")
        self.category.save()
        self.blog = Blog_post(title='title', content='content', category=self.category)
        self.blog.save()
        

    def test_blog_is_created(self):
        url = "/blog/edit_blogs/1"
        data = {'title': ['sajdgjs'], 'content': ['gjsagjdgaj'],'category': ['1']}
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data)

        self.assertEquals(r.status_code, 302)
        assert Blog_post.objects.count() == 1
        