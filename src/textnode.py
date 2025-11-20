from enum import Enum

class TextType(Enum):
    PLAIN = "plain" # "text (plain)"
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