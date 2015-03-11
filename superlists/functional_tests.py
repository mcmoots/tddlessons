# Functional tests for TDD tutorial
import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        # Add extra wait time b/c the book told me to.
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # NB: Any method starting with 'test' will be run by test runner
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        
        # Page should announce itself as an app that makes lists of sea creatures
        self.assertIn('Sea Creatures', self.browser.title)
        self.fail("This test isn't finished yet! Write moar test!")

        # User should be prompted to enter a sea creature

        # User types "vampire squid" into a text box

        # User hits enter, the page updates and lists
        # "1: Vampire squid" as an item in the sea creature list

        # There will still be a text box inviting her to add another item.
        # Enters "echinoderm", and page updates to show both sea creatures.

        # Site generates a unique URL for this list
        # with some explanatory text about it

        # Visiting the URL results in the list of sea creatures reappearing



if __name__ == '__main__':
    unittest.main(warnings='ignore')
