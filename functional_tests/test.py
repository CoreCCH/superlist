import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
            super().setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith 聽到一個很酷的代辦事項app
        # 去察看首頁
        self.browser.get(self.server_url)

        # 她發現網頁標題與標頭顯示待辦事項清單
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)
        
        # 她馬上受邀輸入一個代辦事項
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她在文字方塊輸入"購買孔雀羽毛"
        inputbox.send_keys('Buy peacock feathers')

        # 當她按下enter時，她會被帶到新的ULR
        # 現在網頁列出 1: Buy peacock feathers
        # 一個待辦清單的項目
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists.+')
        
   
        # 此時仍然有一個文字方塊，讓她可以加入另一個項目
        # 她輸入 "使用孔雀羽毛來製作一隻蒼蠅"
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        

        # 網頁再次更新時，現在她的清單有這兩個項目
        self.check_for_row_in_list_table('1: Buy peacock feathers') #檢查這個字符串是否出現在網頁上的一個表格中
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly') #檢查這個字符串是否出現在網頁上的一個表格中
        # 她前往那個URL -她的代辦清單仍在那裡

        # 新的使用者Francis來到網站

        ## 我們使用一個新的瀏覽器工作階段來確保
        ## Edith的任何資訊都不會被cookies等機制送出
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis 造訪首頁。沒有任何 Edith 的清單跡象
        self.browser.get(self.server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # Francis輸入一個新項目，做出一個新清單
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis取得自己的URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 他們滿意地上床睡覺

    def test_layout_and_styling(self):
        #Edith 前往首頁
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        #她發現輸入方塊已妥善被至中
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )

