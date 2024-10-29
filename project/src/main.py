import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from markdown_parser import markdown_to_html_node, extract_title
from textnode import TextNode, TextType
from htmlnode import LeafNode
import shutil

public_directory = 'public'

items = os.listdir(public_directory)
for item in items:
    item_path = os.path.join(public_directory, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    os.mkdir(dst)

    items = os.listdir(src)

    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {item}")
        else:
            copy_static(src_path, dst_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_content_node = markdown_to_html_node(markdown_content)
    html_content = html_content_node.to_html()
    print("HTML_Content:")
    print(html_content)

    title = extract_title(markdown_content)

    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w') as output_file:
        output_file.write(full_html)


def main():
    items = os.listdir(public_directory)
    for item in items:
        item_path = os.path.join(public_directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()

