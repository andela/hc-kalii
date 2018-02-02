from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    '''
    This model contains the particulars of the category
    a blog post can belong too
    '''

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Blog_post(models.Model):
    '''
    This model contains the particulars of the blog post created
    '''
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, 
                                on_delete = models.CASCADE)
    user = models.ForeignKey(User, 
                            blank=True, 
                            null=True, 
                            on_delete= models.CASCADE)

    def __str__(self):
        '''Representation of string output from the database'''
        return self.title


