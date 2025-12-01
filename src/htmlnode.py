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
        raise NotImplementedError("to_html method not implemented")  # Placeholder. Child classes should override this method.
    
    def props_to_html(self):
        """
        Return a formatted string representing the HTML attributes of the node.
        """
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):   # A Child of HTMLNode representing nodes without children
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        # Use the super() function to call the constructor of the HTMLNode class.
        # Add a .to_html() method that renders a leaf node as an HTML string (by returning a string)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value  # return as raw text. 
        # else render an HTML tag.
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):  # A Child of HTMLNode representing nodes with children
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTMLL no children")
        children_html = ""
        # Otherwise, return a string representing the HTML tag of the node and its children.
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNote({self.tag}, children: {self.children}, {self.props})"
