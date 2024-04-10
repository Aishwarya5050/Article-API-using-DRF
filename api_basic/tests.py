from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from .models import Article

class ArticleCreateTestCase(APITestCase):
    def test_create_article(self):
        self.data={
            'Title' : 'Title',
            'Author' : 'Author',
            'Email' : 'Email',
            'Date' : 'Date',
            
        }
    def tearDown(self):
        return super().tearDown()