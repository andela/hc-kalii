from hc.test import BaseTestCase
from hc.front.models import Category, Blog_post

class UpdateBlogTest(BaseTestCase):
    def setUp(self):
        super(UpdateBlogTest, self).setUp()
        Category.objects.create(name="test category")
        self.category = Category.objects.get(name="test category")
        Blog_post.objects.create(title='title', content='content', category=self.category)
        self.blog = Blog_post.objects.get(title='title')
        self.url = ("/blog/edit_blogs/%s" % self.blog.id)
        

    def test_blog_is_edited(self):     
        data = {'title':'title2', 'content':'contents', 'category': self.category.id}       
        r = self.client.post(self.url, data)
        self.assertEquals(r.status_code, 302)
        self.blog.refresh_from_db()
        self.assertEquals(self.blog.title, "title2")
