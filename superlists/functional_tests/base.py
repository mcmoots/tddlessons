# Functional tests for TDD tutorial
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        # Add extra wait time b/c the book told me to.
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()
    

    def check_for_item_in_list(self, item_text):
        creaturelist = self.browser.find_element_by_id('id_list')
        items = creaturelist.find_elements_by_tag_name('li')
        self.assertIn(item_text, [item.text for item in items])
