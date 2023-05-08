from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item
import re

class SmokeTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        excepted_html = render_to_string('home.html', request=request)

        # 忽略CSRF的value進行比對
        response_html = self.ignore_csrf_token(response.content.decode())
        excepted_html = self.ignore_csrf_token(excepted_html)

        self.assertEqual(response_html, excepted_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        # 檢查首頁是否有新增項目        
        self.assertIn('A new list item', response.content.decode())
        excepted_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )

        # 忽略CSRF的value進行比對
        response_html = self.ignore_csrf_token(response.content.decode())
        excepted_html = self.ignore_csrf_token(excepted_html)

        self.assertEqual(response_html, excepted_html)

    @staticmethod
    def ignore_csrf_token(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(html_code, '', csrf_regex)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')