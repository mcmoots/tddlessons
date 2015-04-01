# Functional tests for TDD tutorial
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Myrtle accidentally tries to submit an empty list item.
        # She hits Enter on the empty input box.

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank.
    

        # She tries again with some text for the item, and now it works.

        # Then she submits another blank list item!

        # She gets a similar warning on the list page.

        # And she can correct it by filling in some text.
        self.fail('Test not written yet!')
