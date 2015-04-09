# Functional tests for TDD tutorial
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Myrtle accidentally tries to submit an empty list item.
        # She hits Enter on the empty input box.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank.
        problem_element = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(problem_element.text, "\U0001f42c No empty sea creatures allowed!" )

        # She tries again with some text for the item, and now it works.
        self.get_item_input_box().send_keys('lamprey\n')
        self.check_for_item_in_list('1: lamprey')

        # Then she submits another blank list item!
        self.get_item_input_box().send_keys('\n')

        # She gets a similar warning on the list page.
        self.check_for_item_in_list('1: lamprey')
        problem_element = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(problem_element.text, "\U0001f42c No empty sea creatures allowed!" )

        # And she can correct it by filling in some text.
        self.get_item_input_box().send_keys('anglerfish\n')
        self.check_for_item_in_list('1: lamprey')
        self.check_for_item_in_list('2: anglerfish')


    def test_cannot_add_duplicate_items(self):
        # Myrtle starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('brachiopods\n')
        self.check_for_item_in_list('1: brachiopods')

        # then she accidentally enters more brachiopods
        self.get_item_input_box().send_keys('brachiopods\n')

        # she sees a helpful error message
        self.check_for_item_in_list('1: brachiopods')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You have already listed that sea creature")
