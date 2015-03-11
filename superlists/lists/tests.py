from django.test import TestCase

# Create your tests here.

class SillyTest(TestCase):

    def test_bad_math(self):
        self.assertEqual(2+2, 5)
