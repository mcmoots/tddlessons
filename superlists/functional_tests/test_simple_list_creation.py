# Functional tests for TDD tutorial
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        
        # Our first user is Myrtle. Myrtle visits the home page.
        # Page should announce itself as an app that makes lists of sea creatures
        self.assertIn('Sea Creatures', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Sea Creatures', header_text)

        # User should be prompted to enter a sea creature
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a sea creature'
        )

        # Myrtle types "vampire squid" into a text box and hits enter
        inputbox.send_keys('vampire squid')
        inputbox.send_keys(Keys.ENTER)

        # Myrtle is taken to a new URL, which lists "1: vampire squid"
        # as an item in a list
        myrtle_list_url = self.browser.current_url
        self.assertRegex(myrtle_list_url, '/lists/.+')
        self.check_for_item_in_list('1: vampire squid')

        # There will still be a text box inviting Myrtle to add another item.
        # Enters "echinoderm", and page updates to show both sea creatures.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('echinoderm')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_item_in_list('1: vampire squid')
        self.check_for_item_in_list('2: echinoderm')

        # now a new user, Archibald, visits the home page
        # he shouldn't see anything of Myrtle's

        ## use a new browser session so nothing bleeds through from Myrtle
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('vampire squid', page_text)
        self.assertNotIn('echinoderm', page_text)

        # Archibald starts a new list by entering a new sea creature.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('herring')
        inputbox.send_keys(Keys.ENTER)

        # Archibald gets his own URL
        archibald_list_url = self.browser.current_url
        self.assertRegex(archibald_list_url, '/lists/.+')
        self.assertNotEqual(archibald_list_url, myrtle_list_url)

        # Still no trace of Myrtle's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('vampire squid', page_text)
        self.assertIn('herring', page_text)

