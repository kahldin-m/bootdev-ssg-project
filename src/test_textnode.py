import unittest

from textnode import TextNode, TextType, text_node_to_html_node # type: ignore


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Click here for Google", TextType.TEXT, "https://www.google.com")
        node2 = TextNode("Click here for Google", TextType.TEXT, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_for_text_type(self):
        for text_type in TextType:
            node = TextNode("Sample", text_type)
            self.assertEqual(node.text_type, text_type)
            # print(f"Created TextNode with type: {text_type}")

    def test_repr(self):
        node = TextNode("Sample", TextType.ITALIC)
        expected_repr = "TextNode('Sample', TextType.ITALIC)"
        self.assertEqual(repr(node), expected_repr)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url="https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.example.com/image.png", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

if __name__ == "__main__":
    unittest.main()