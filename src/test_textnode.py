import unittest

from textnode import TextNode, TextType # type: ignore


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Sample", TextType.ITALIC)
        expected_repr = "TextNode(Sample, italic, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_for_text_type(self):
        for text_type in TextType:
            node = TextNode("Sample", text_type)
            self.assertEqual(node.text_type, text_type)
            print(f"Created TextNode with type: {text_type}")

if __name__ == "__main__":
    unittest.main()