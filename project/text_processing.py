from src.textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        current_type = TextType.TEXT
        start = 0

        while start < len(text):
            end = text.find(delimiter, start)

            if end == -1:
                if current_type != TextType.TEXT:
                    raise ValueError(f"Unmatched delimiter {delimiter} in text: {text}")
                new_nodes.append(TextNode(text[start:], TextType.TEXT))
                break

            if end > start:
                new_nodes.append(TextNode(text[start:end], current_type))

            start = end + len(delimiter)
            current_type = text_type if current_type == TextType.TEXT else TextType.TEXT

    return new_nodes

def split_nodes_image(old_nodes):
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        segments = re.split(image_pattern, text)


        for i in range(0, len(segments), 3):
            if segments[i]:
                new_nodes.append(TextNode(segments[i], TextType.TEXT))
            if i + 1 < len(segments):
                new_nodes.append(TextNode(segments[i + 1], TextType.IMAGE, segments[i + 2]))

    return new_nodes

def split_nodes_link(old_nodes):
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        segments = re.split(link_pattern, text)

        for i in range(0, len(segments), 3):
            if segments[i]:
                new_nodes.append(TextNode(segments[i], TextType.TEXT))
            if i + 1 < len(segments):
                new_nodes.append(TextNode(segments[i + 1], TextType.LINK, segments[i + 2]))

    return new_nodes
