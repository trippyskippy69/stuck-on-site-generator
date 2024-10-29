import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="div", value="", children=[], props={})
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="a", value="Link", children=[], props={"href": "https://www.google.com"})
        expected_string = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected_string)

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(tag="a", value="Link", children=[], props={"href": "https://www.google.com", "target": "_blank"})
        expected_string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_string)

class TestLeafNode(unittest.TestCase):

    def test_leaf_node_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode('p', None)

    def test_leaf_node_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_node_with_tag_and_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        expected_html = '<a href="https://www.example.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_html)


if __name__ == '__main__':
    unittest.main()
