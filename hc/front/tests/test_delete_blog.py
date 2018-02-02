from hc.test import BaseTestCase
from hc.front.models import Category, Blog_post

class DeleteBlogTest(BaseTestCase):
    def setUp(self):
        super(DeleteBlogTest, self).setUp()
        self.category = Category(name="test category")
        self.category.save()
        Blog_post.objects.create(title='title', content='content', category=self.category)
        self.blog = Blog_post.objects.get(title='title')
        self.url = ("/blog/delete_blog/%s" % self.blog.id)
        

    def test_blog_is_deleted(self):            
        r = self.client.post(self.url)
        self.assertEquals(r.status_code, 302)
        assert Blog_post.objects.count() == 0