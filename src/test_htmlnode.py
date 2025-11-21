import unittest

from htmlnode import HTMLNode # type: ignore


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello, World!", children=[], props={"attribute": "intro"})
        expected_repr = "HTMLNode(p, Hello, World!, [], {'attribute': 'intro'})"
        self.assertEqual(repr(node), expected_repr)
        print(f"Created HTMLNode with repr: {repr(node)}")

    def test_props_attributes(self):
        node_with_props = HTMLNode(tag="a", value="Link", props={"href": "https://www.google.com", "target": "_blank"})
        expected_props_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node_with_props.props_to_html(), expected_props_html)
        print(f"Created HTMLNode with props: {repr(node_with_props)}")

        node_without_props = HTMLNode(tag="p", value="No props here")
        self.assertEqual(node_without_props.props_to_html(), "")
        print(f"Created HTMLNode without props: {repr(node_without_props)}")

    def test_header_node(self):
        header_node = HTMLNode(tag="h1", value="Header text")
        expected_repr = "HTMLNode(h1, Header text, None, None)"
        self.assertEqual(repr(header_node), expected_repr)
        print(f"Created Header HTMLNode: {repr(header_node)}")

if __name__ == "__main__":
    unittest.main()