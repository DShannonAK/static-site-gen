import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_props_to_html_empty(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), "")    

    def test_init(self):
        node = HTMLNode()
        self.assertTrue(node.tag == None and node.value == None and node.children == None and node.props == None)

if __name__ == "__main__":
    unittest.main()