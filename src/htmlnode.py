class HTMLNode(object):
    def __init__(self, tag=None, value=None, children=None, props=None):
        # A striong representing the valuie of the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.tag = tag

        # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.value = value

        # A list of child HTMLNode object represnting children of this node
        self.children = children

        # A dictionairy of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props

    def to_html(self):
        raise NotImplementedError  # Placeholder. Child classes should override this method.
    
    def props_to_html(self):
        """
        Should return a formatted string representing the HTML attributes of the node.
        """
        return f' href="{self.props["href"]}" target="{self.props["target"]}"' if self.props else ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"