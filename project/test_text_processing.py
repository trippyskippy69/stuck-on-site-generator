import unittest
from text_processing import split_nodes_delimiter, split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This **is** bold **text**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" bold ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_no_split(self):
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [node]
        self.assertEqual(result, expected)

    def test_empty_parts(self):
        node = TextNode("word**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("word", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_missing_closing_delimiter(self):
        node = TextNode("This is *italic", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_split_nodes_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and more text."
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])

        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and more text.", TextType.TEXT),
        ]
        
        self.assertEqual(result, expected_result)

    def test_split_nodes_image(self):
        text = "Text with an image ![alt text](https://example.com/image.png) and more."
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])

        expected_result = [
            TextNode("Text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and more.", TextType.TEXT),
        ]
        
        self.assertEqual(result, expected_result)

