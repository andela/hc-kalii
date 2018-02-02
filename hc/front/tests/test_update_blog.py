from hc.test import BaseTestCase
from hc.front.models import Category, Blog_post

class UpdateBlogTest(BaseTestCase):
    def setUp(self):
        super(UpdateBlogTest, self).setUp()
        self.category = Category(name="test category")
        self.category.save()
        Blog_post.objects.create(title='title', content='content', category=self.category)
        self.blog = Blog_post.objects.get(title='title')
        self.url = ("/blog/edit_blogs/%s" % self.blog.id)
        

    def test_blog_is_created(self):
        data = {'title': ['sajdgjs'], 'content': ['gjsagjdgaj'],'category': ['1']}
        r = self.client.post(self.url, data)

        self.assertEquals(r.status_code, 302)
        assert Blog_post.objects.count() == 1

