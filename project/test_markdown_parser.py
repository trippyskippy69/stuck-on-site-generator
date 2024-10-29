from markdown_parser import extract_markdown_images, extract_markdown_links
import unittest
class TestMarkdownParser(unittest.TestCase):
   def test_extract_markdown_images(self):
       text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
       result = extract_markdown_images(text)
       expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
       self.assertEqual(result, expected, f"Expected {expected}, but got {result}")

       self.assertEqual(extract_markdown_images(""), [], "Should return an empty list for empty string")
       self.assertEqual(extract_markdown_images("No images here"), [], "Should return an empty list when no images are present")
       self.assertEqual(extract_markdown_images("![img1](url1) ![img2](url2)"), [("img1", "url1"), ("img2", "url2")], "Should extract multiple images correctly")
       self.assertEqual(extract_markdown_images("![img with spaces](url with spaces)"), [("img with spaces", "url with spaces")], "Should handle spaces in alt text and URL")

   def test_extract_markdown_links(self):
       text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
       result = extract_markdown_links(text)
       expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
       self.assertEqual(result, expected, f"Expected {expected}, but got {result}")

       self.assertEqual(extract_markdown_links(""), [], "Should return an empty list for empty string")
       self.assertEqual(extract_markdown_links("No links here"), [], "Should return an empty list when no links are present")
       self.assertEqual(extract_markdown_links("[link1](url1) [link2](url2)"), [("link1", "url1"), ("link2", "url2")], "Should extract multiple links correctly")
       self.assertEqual(extract_markdown_links("[link with spaces](url with spaces)"), [("link with spaces", "url with spaces")], "Should handle spaces in link text and URL")

   def test_bold(self):
       text = "Just **bold** here."
       expected_output = [
           TextNode("Just ", TextType.TEXT),
           TextNode("bold", TextType.BOLD),
           TextNode(" here.", TextType.TEXT)
       ]
       self.assertEqual(text_to_textnodes(text), expected_output)

   def test_italic_and_code(self):
       text = "Here's *italic* and `code`."
       expected_output = [
           TextNode("Here's ", TextType.TEXT),
           TextNode("italic", TextType.ITALIC),
           TextNode(" and ", TextType.TEXT),
           TextNode("code", TextType.CODE),
           TextNode(".", TextType.TEXT)
       ]
       self.assertEqual(text_to_textnodes(text), expected_output)

   def test_image(self):
       text = "Pic ![a cat](https://example.com/cat.jpg)"
       expected_output = [
           TextNode("Pic ", TextType.TEXT),
           TextNode("a cat", TextType.IMAGE, "https://example.com/cat.jpg")
       ]
       self.assertEqual(text_to_textnodes(text), expected_output)

   def test_link(self):
       text = "Visit [Boot.dev](https://boot.dev)"
       expected_output = [
           TextNode("Visit ", TextType.TEXT),
           TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
       ]
       self.assertEqual(text_to_textnodes(text), expected_output)

   def test_plain_text(self):
       text = "Just a simple sentence."
       expected_output = [
           TextNode("Just a simple sentence.", TextType.TEXT)
       ]
       self.assertEqual(text_to_textnodes(text), expected_output)

   def test_basic_blocks(self):
        markdown = "# Heading\n\nParagraph\n\n* List item"
        expected = ["# Heading", "Paragraph", "* List item"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_extra_newlines(self):
        markdown = "Block 1\n\n\n\nBlock 2\n\n\nBlock 3"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace(self):
        markdown = "  Block 1  \n\n  Block 2  "
        expected = ["Block 1", "Block 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block(self):
        markdown = "Just one block"
        expected = ["Just one block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("### Heading 3"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")
        self.assertEqual(block_to_block_type("####### Not a heading"), "paragraph")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), "code")
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), "code")

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1"), "unordered_list")
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2\n* Item 3"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), "unordered_list")
        self.assertEqual(block_to_block_type("* Item 1\n- Item 2"), "unordered_list")

        self.assertEqual(block_to_block_type("Item 1\nItem 2"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), "ordered_list")
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), "ordered_list")

        long_list = "\n".join([f"{i}. Item {1}" for i in range(1, 12)])
        self.assertEqual(block_to_block_type(long_list), "ordered_list")


        self.assertNotEqual(block_to_block_type("1. First item\n1. Second item"), "ordered_list")
        self.assertNotEqual(block_to_block_type("1. First item\n3. Third item"), "ordered_list")
        self.assertNotEqual(block_to_block_type("1 First item"), "ordered_list")
        self.assertNotEqual(block_to_block_type("1.First item"), "ordered_list")

        self.assertNotEqual(block_to_block_type("This is item 1. This is item 2."), "ordered_list")

    def test_paragraph(self):

        self.assertEqual(block_to_block_type("This is a simple paragraph."), "paragraph")
        self.assertEqual(block_to_block_type("This is a paragraph\nwith multiple lines."), "paragraph")


        self.assertEqual(block_to_block_type("This # is not a heading"), "paragraph")
        self.assertEqual(block_to_block_type("This * is not a list item"), "paragraph")
        self.assertEqual(block_to_block_type("This 1. is not an ordered list"), "paragraph")
        self.assertEqual(block_to_block_type("This > is not a quote"), "paragraph")

        self.assertEqual(block_to_block_type("This paragraph has **bold** and *italic* text."), "paragraph")
        self.assertEqual(block_to_block_type("This paragraph has a [link](https://example.com)."), "paragraph")

        self.assertEqual(block_to_block_type(""), "paragraph")

if __name__ == "__main__":
    unittest.main()

def test_text_to_children():
    text = "This is **bold**"
    children = text_to_children(text)
    
    assert len(children) == 2
    bold_node = children[1]
    assert bold_node.tag == "b"
    assert bold_node.children[0].text == "bold"
    text = "Hello *italic* and **bold**"
    children = text_to_children(text)
    assert len(children) == 4

class TestExtractTitle(unittest.TestCase):

    def test_extract_title_normal_case(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_no_space(self):
        self.assertEqual(extract_title("#Hello"), "Hello")

    def test_extract_title_no_header(self):
        with self.assertRaises(NoH1HeaderFound):
            extract_title("## Subheader\nNo h1 here")

    def test_extract_title_with_whitespace(self):
        self.assertEqual(extract_title("#  Hello World  "), "Hello World")

if __name__ == '__main__':
    unittest.main()
