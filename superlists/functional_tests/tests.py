#!/usr/bin/env python

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        inputbox.send_keys('Buy xbox one x')
        inputbox.send_keys(Keys.ENTER)

        user_1_list_url = self.browser.current_url
        self.assertRegex(user_1_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy xbox one x')

        # new user
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy xbox one x', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        user_2_list_url = self.browser.current_url
        self.assertRegex(user_2_list_url, '/lists/.+')
        self.assertNotEqual(user_1_list_url, user_2_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy xbox one x', page_text)
        self.assertIn('Buy milk', page_text)
