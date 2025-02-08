from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "**", "b"
    ITALIC = "*", "i"
    CODE = "```", "code"
    LINK = "[link]", "a"
    IMAGE = "!", "img"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    node = LeafNode(text_node.text_type.value, text_node.text)
    if text_node.text_type == TextType.TEXT:
        node.tag = None
    else:
        node.tag = text_node.text_type.value[1]
        if text_node.text_type == TextType.IMAGE:
            node.value = ""
            node.props = {"src" : text_node.url, "alt" : text_node.text}
        elif text_node.text_type == TextType.LINK:
            node.props = {"href" : text_node.url}
    return node #$f"<{node.tag}{node.props}>{node.value}</{node.tag}>"