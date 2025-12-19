import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode # type: ignore


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://www.fakenews.net"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://www.fakenews.net"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could go outside",
        )
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, "I wish I could go outside")
        self.assertIsNone(node.children, None)
        self.assertIsNone(node.props, None)
    
    def test_repr(self):
        node = HTMLNode(tag="p", value="No rats in Paris!", children=None, props={"class": "primary"})
        expected_repr = "HTMLNode(p, No rats in Paris!, children: None, {'class': 'primary'})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_attributes(self):
        node_with_props = HTMLNode(tag="a", value="Link", props={"href": "https://www.google.com", "target": "_blank"})
        expected_props_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node_with_props.props_to_html(), expected_props_html)

        node_without_props = HTMLNode(tag="p", value="No props here")
        self.assertEqual(node_without_props.props_to_html(), "")

    def test_header_node(self):
        header_node = HTMLNode(tag="h1", value="Header text")
        expected_repr = "HTMLNode(h1, Header text, children: None, None)"
        self.assertEqual(repr(header_node), expected_repr)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!")
        node.props = {"href": "https://www.google.com", "target": "_blank"}
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

# Test all the edge cases you can think of, including nesting ParentNode objects inside of one another, multiple children, and no children.
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),\
                LeafNode(None, "Normal text"),
                LeafNode("i", "Itallic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Itallic text</i>Normal text</p>",
        )
        # print(repr(node))

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Itallic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual
        (
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>Itallic text</i>Normal text</h2>",
        )
        # print(repr(node))

if __name__ == "__main__":
    unittest.main()