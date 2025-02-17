from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node
import os, shutil

def main():
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

def copy_static(source, destination):
    if verify(source) and verify(destination):
        delete(destination)
        files = os.listdir(source)
        for file in files:
            source_path = os.path.join(source, file)
            destination_path = os.path.join(destination, file)
            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
            else:
                os.makedirs(destination_path)
                copy_static(source_path, destination_path)
            
def verify(path):
    if not os.path.exists(path):
        raise ValueError(f"Invalid path: {path}")
    return True
def delete(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            delete(file_path)
            os.rmdir(file_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("Title not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read(from_path)
    template = read(template_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dir = os.path.dirname(dest_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = open(dest_path, "w")
    file.write(html)
    file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Invalid path: {dir_path_content}")
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    files = os.listdir(dir_path_content)
    for file in files:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_path)

def read(path):
    file = open(path)
    content = file.read()
    file.close()
    return content

main()