import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        title = "# Hello"
        no_title = "Hello"
        self.assertEqual(extract_title(title), no_title)
        self.assertRaises(Exception, extract_title, no_title)