import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from main import text_node_to_html_node
from text_to_html import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_property(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text, "This is a text node")

    def test_url_property_with_url(self):
        node = TextNode("Click here", "link", "https://www.example.com")
        self.assertEqual(node.url, "https://www.example.com")

    def test_url_property_without_url(self):
        node = TextNode("Just text", "plain")
        self.assertIsNone(node.url)

    def test_inequality(self):
        node1 = TextNode("Text", TextType.BOLD)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_text_type_property(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text_type, "bold")

    def test_url_property_default(self):
        node = TextNode("Just text", "plain")
        self.assertIsNone(node.url)
    
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello, world!")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})

    def test_text_node_to_html_node_invalid_type(self):
        text_node = TextNode("Invalid", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_text_node_to_html_node_non_textnode_input(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node("Not a TextNode")

if __name__ == "__main__":
    unittest.main()
