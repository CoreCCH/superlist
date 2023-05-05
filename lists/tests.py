from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page

class SmokeTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>')) # 希望開頭有html標籤
        self.assertIn(b'<title>To-Do list</title>', response.content) # 希望中間某處有title標籤，並有"To-Do list"
        self.assertTrue(response.content.endswith(b'</html>')) # 希望結束有/html標籤