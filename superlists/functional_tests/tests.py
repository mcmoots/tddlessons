# Functional tests for TDD tutorial
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    
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

    # NB: Any method starting with 'test' will be run by test runner
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        
        # Page should announce itself as an app that makes lists of sea creatures
        self.assertIn('Sea Creatures', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Sea Creatures', header_text)

        # User should be prompted to enter a sea creature
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a sea creature'
        )

        # User types "vampire squid" into a text box and hits enter
        inputbox.send_keys('vampire squid')
        inputbox.send_keys(Keys.ENTER)

        # The page should update so that
        # "1: Vampire squid" is an item in the sea creature list
        self.check_for_item_in_list('1: vampire squid')

        # There will still be a text box inviting her to add another item.
        # Enters "echinoderm", and page updates to show both sea creatures.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('echinoderm')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_item_in_list('1: vampire squid')
        self.check_for_item_in_list('2: echinoderm')

        # Site generates a unique URL for this list
        # with some explanatory text about it

        # Visiting the URL results in the list of sea creatures reappearing

        # todo: test should clean up after itself
        self.fail("This test isn't finished yet! Write moar test!")

