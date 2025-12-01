import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
        result = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(result, [node])

    def test_multiple_nodes_mix(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        node2 = TextNode("**Bold text only**", TextType.BOLD)
        result = split_nodes_delimiter([node, node2], '`', TextType.CODE)
        expected = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            node2,
        ]
        self.assertEqual(result, expected)

    def test_one_delimiter(self):
        node = TextNode("This is a `code` block", TextType.TEXT)
        result = split_nodes_delimiter([node], '`', TextType.CODE)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This is a `code` block with multiple `code` segments", TextType.TEXT)
        result = split_nodes_delimiter([node], '`', TextType.CODE)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block with multiple ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" segments", TextType.TEXT),
        ]

    def test_broken_markdown(self):
        node = TextNode("This is a text with __open delimiter and no close", TextType.TEXT)
        with self.assertRaisesRegex(Exception, "Invalid Markdown: missing delimiter"):
            split_nodes_delimiter([node], '__', TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()