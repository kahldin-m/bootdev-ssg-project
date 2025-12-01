from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text" # "text (plain)"
    BOLD = "bold" # "**Bold text**"
    ITALIC = "italic" # "_Italic text_"
    CODE = "code" # "`Code text`"
    LINK = "link" # "[anchor text](url)"
    IMAGE = "image" # "![alt text](url)"
    

class TextNode(object):
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url} if text_node.url else {})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text} if text_node.url else {"alt": text_node.text})
    raise ValueError(f"Unsupported TextType: {text_node.text_type}")