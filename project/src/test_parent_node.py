import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)

    def test_to_html_basic(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_nested(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("span", "Hello"),
                LeafNode(None, " "),
                LeafNode("em", "World")
            ])
        ])
        self.assertEqual(node.to_html(), "<div><p><span>Hello</span> <em>World</em></p></div>")

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "Hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_multiple_children(self):
        node = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ])
        self.assertEqual(node.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def test_mixed_children(self):
        node = ParentNode("div", [
        LeafNode("p", "Paragraph"),
        ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2")
        ]),
        LeafNode("p", "Another paragraph")
        ])
        expected = "<div><p>Paragraph</p><ul><li>Item 1</li><li>Item 2</li></ul><p>Another paragraph</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_deep_nesting(self):
        node = ParentNode("div", [
        ParentNode("div", [
            ParentNode("div", [
                LeafNode("p", "Deep nested paragraph")
            ])
        ])
        ])
        expected = "<div><div><div><p>Deep nested paragraph</p></div></div></div>"
        self.assertEqual(node.to_html(), expected)
