from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith 聽到一個很酷的代辦事項app
        # 去察看首頁
        self.browser.get('http://localhost:8000')

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

        # 當她按下enter時，網頁會更新，現在網頁列出
        # "1:購買孔雀羽毛"，一個代辦事項清單項目
        inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(3) # 等3秒

        # 此時仍然有一個文字方塊，讓她可以加入另一個項目
        # 她輸入 "使用孔雀羽毛來製作一隻蒼蠅"
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(3) # 等3秒
        
        # 網頁再次更新時，現在她的清單有這兩個項目
        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn(
            '1: Buy peacock feathers' , [row.text for row in rows]
        )
        self.assertIn(
            '2: Use peacock feathers to make a fly' , [row.text for row in rows]
        )

        

        self.fail('Finish the Test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')