from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith 聽到一個很酷的代辦事項app
        # 去察看首頁
        self.browser.get('http://localhost:8000')

        # 她發現網頁標題與標頭顯示待辦事項清單
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the Test!')

        # 她馬上受邀輸入一個代辦事項

if __name__ == '__main__':
    unittest.main(warnings='ignore')