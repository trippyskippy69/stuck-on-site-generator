import re
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from src.text_to_html import text_node_to_html_node

def text_to_textnodes(text):
    pattern = r"(!\[([^\[\]]*)\]\(([^\(\)]*)\))|(\[([^\[\]]*)\]\(([^\(\)]*)\))|(\*\*([^*]+)\*\*)|(\*([^*]+)\*)|(`([^`]+)`)|([^*!`\[\]]+)"
    textnodes = []
    matches = re.finditer(pattern, text)

    for match in matches:
        if match.group(1):
            alt_text, url = match.group(2), match.group(3)
            textnodes.append(TextNode(alt_text, TextType.IMAGE, url))
        elif match.group(4):
             link_text, url = match.group(5), match.group(6)
             textnodes.append(TextNode(link_text, TextType.LINK, url))
        elif match.group(7):
             bold_text = match.group(8)
             textnodes.append(TextNode(bold_text, TextType.BOLD))
        elif match.group(9):
             italic_text = match.group(10)
             textnodes.append(TextNode(italic_text, TextType.ITALIC))
        elif match.group(11):
             code_text = match.group(12)
             textnodes.append(TextNode(code_text, TextType.CODE))
        elif match.group(13):
             plain_text = match.group(13)
             textnodes.append(TextNode(plain_text, TextType.TEXT))


    return textnodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def split_blocks(markdown):
    print("Splitting markdown:")
    print(markdown)
    
    lines = markdown.split('\n')
    print("Lines after split:")
    print(lines)

    blocks = []
    current_block = []

    for line in lines:
        line = line.strip()
        if line:
            current_block.append(line)
        elif current_block:
            block_content = '\n'.join(line for line in current_block if line.strip())
            print(f"Adding block: {block_content}")
            blocks.append(block_content)
            current_block = []

    if current_block:
        block_content = '\n'.join(line for line in current_block if line.strip())
        print(f"Adding final block: {block_content}")
        blocks.append(block_content)

    print("Final blocks:")
    print(blocks)
    return blocks

def block_to_block_type(block):
    print(f"\nAnalyzing block: 

    count = 0
    if block.startswith('#'):
        for char in block:
            if char == '#':
                count += 1
            else:
                break
        print(f"Found {count} # characters")
    if 1 <= count <= 6 and block[count] == ' ' and len(block) > count + 1:
        return "heading"

    if block.startswith('```') and block.endswith('```'):
        return "code"


    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return "quote"

    if all(line.strip().startswith(('*', '-')) for line in lines):
        return "unordered_list"

    if all(line.strip().split('.')[0].isdigit() for line in lines):
        numbers = [int(line.strip().split('.')[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return "ordered_list"

    block_type = "paragraph"  # default
    print(f"Block type determined: {block_type}")
    return block_type


    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = split_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            content = extract_heading_content(block)
            heading_node = HTMLNode(f"h{level}", content, [])
            block_nodes.append(heading_node)

        elif block_type == "code":
             content = extract_code_content(block)
             code_node = HTMLNode("code", content, [])
             pre_node = HTMLNode("pre", "", [code_node])
             block_nodes.append(pre_node)

        elif block_type == "quote":
             content = extract_quote_content(block)
             quote_node = HTMLNode("blockquote", content, [])
             block_nodes.append(quote_node)

        elif block_type == "unordered_list":
            list_node = HTMLNode("ul", "", [])
            lines = block.split("\n")
            for line in lines:
                if not line.strip():
                    continue
                content = line.strip("* ").lstrip("- ").strip()
                children = text_to_children(content)
                li_node = HTMLNode("li", "", children)
                list_node.children.append(li_node)
            block_nodes.append(list_node)

        elif block_type == "ordered_list":
            list_node = HTMLNode("ol", "", [])
            lines = block.split("\n")
            for line in lines:
                if not line.strip():
                    continue
                content = line.strip()
                for i in range(len(content)):
                    if content[i] == ".":
                        content = content[i + 1:].strip()
                        break

                children = text_to_children(content)
                li_node = HTMLNode("li", "", children)
                list_node.children.append(li_node)
            block_nodes.append(list_node)

        elif block_type == "paragraph":
             children = text_to_children(block)
             p_node = HTMLNode("p", "", children)
             block_nodes.append(p_node)
    return HTMLNode("div", "",  block_nodes)

def extract_heading_content(block):
    index = 0
    while index < len(block) and block[index] == '#':
        index += 1
    if index < len(block) and block[index] == ' ':
        index += 1
    return block[index:].strip()

def extract_code_content(block):
    if block.startswith('```') and block.endswith('```'):
        return block[3:-3].strip()
    return block.strip()

def extract_quote_content(block):
    lines = block.split('\n')
    quote_lines = []
    for line in lines:
        if line.startswith('> '):
            quote_lines.append(line[2:])
        elif line.startswith('>'):
            quote_lines.append(line[1:])
    return '\n'.join(quote_lines).strip()
class NoH1HeaderFound(Exception):
    pass

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("#"):
            return line[1:].strip()

    raise NoH1HeaderFound("No H1 header found in the provided markdown.")
