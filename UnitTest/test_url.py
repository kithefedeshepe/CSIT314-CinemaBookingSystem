from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Cinemabooking.views import 

class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self): 
        url = reverse('list')
        self.assertEqual(resolve(url).func, projcet_list)

    def test_add_url_is_resolved(self): 
        url = reverse('add')
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)

     def test_detail_url_is_resolved(self): 
        url = reverse('detail', args['some-slug'])
        self.assertEqual(resolve(url).func, Project_detail)