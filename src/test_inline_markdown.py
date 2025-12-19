import unittest

from textnode import TextNode, TextType
from inline_markdown import (extract_markdown_images, extract_markdown_links,
                             split_nodes_delimiter, split_nodes_image, split_nodes_link,
                             text_to_textnodes)


class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [mobilize](https://www.youtube.com/watch?v=dGAbvGftjVc)"
        )
        self.assertListEqual([("mobilize", "https://www.youtube.com/watch?v=dGAbvGftjVc")], matches)

    def test_extract_md_links_with_images(self):
        matches = extract_markdown_links(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [mobilize](https://www.youtube.com/watch?v=dGAbvGftjVc)"
        )
        self.assertListEqual([("mobilize", "https://www.youtube.com/watch?v=dGAbvGftjVc")], matches)

    def test_extract_md_images_with_links(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [mobilize](https://www.youtube.com/watch?v=dGAbvGftjVc)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extrack_md_images_with_spaces(self):
        matches = extract_markdown_images(
            "A text with an ![alt text] and space between URL: (https://i.imgur.com/aKaOqIh.gif)"
        )
        self.assertListEqual([("alt text", "https://i.imgur.com/aKaOqIh.gif")], matches)


class TestSplitNodeFunctions(unittest.TestCase):
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

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

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


    # <>><><><>< TESTING split_image and split_link
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_text_after(self):
            node = TextNode(
                "![image](http://www.unsecureimages.com) this is a link to an unsecure image",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("image", TextType.IMAGE, "http://www.unsecureimages.com"),
                    TextNode(" this is a link to an unsecure image", TextType.TEXT),
                ],
                new_nodes
            )

    def test_split_images_with_mixed_text(self):
        node = TextNode(
            "![image](http://www.unsecureimages.com/mask_image.png) this is a link to an unsecure image ![another image](http://www.unsecureimages.com/magicmops.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "http://www.unsecureimages.com/mask_image.png"),
                TextNode(" this is a link to an unsecure image ", TextType.TEXT),
                TextNode("another image", TextType.IMAGE, "http://www.unsecureimages.com/magicmops.jpg"),
            ],
            new_nodes
        )

    def test_split_images_no_text(self):
        node = TextNode(
            "![image](http://www.unsecureimages.com/mask_image.png)![another image](http://www.unsecureimages.com/magicmops.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "http://www.unsecureimages.com/mask_image.png"),
                TextNode("another image", TextType.IMAGE, "http://www.unsecureimages.com/magicmops.jpg"),
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and an ![random image](https://cdn.Ppixabay.com/photo/2016/09/16/14/10/mask-1674106_1280.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" and an ![random image](https://cdn.Ppixabay.com/photo/2016/09/16/14/10/mask-1674106_1280.jpg)", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_links_no_text(self):
        node = TextNode(
            "[anchor](http://www.unsecureimages.net)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("anchor", TextType.LINK, "http://www.unsecureimages.net"),
            ],
            new_nodes
        )

    def test_split_links_no_link(self):
        node = TextNode(
            "This is just a normal text node without proper links to https://www.youtube.com/",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just a normal text node without proper links to https://www.youtube.com/", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_images_multi_node(self):
        node1 = TextNode(
            "A node with an ![image](www.testimage.com)",
            TextType.TEXT
        )
        node2 = TextNode(
            "A node with a [anchor](www.fake-website.com) and an image ![alt text](www.pandasarecutester.com/panda.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("A node with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.testimage.com"),
                TextNode("A node with a [anchor](www.fake-website.com) and an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "www.pandasarecutester.com/panda.png")
            ],
            new_nodes
        )

    def test_split_links_multi_node(self):
        image_node = TextNode(
            "A node with an ![image](www.testimage.com)",
            TextType.TEXT
        )
        mixed_node = TextNode(
            "A node with a [anchor](www.fake-website.com) and an image ![alt text](www.pandasarecutester.com/panda.png)",
            TextType.TEXT
        )
        plain_node = TextNode(
            "A simple text node",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([image_node, mixed_node, plain_node])
        self.assertListEqual(
            [
                TextNode("A node with an ![image](www.testimage.com)", TextType.TEXT),
                TextNode("A node with a ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "www.fake-website.com"),
                TextNode(" and an image ![alt text](www.pandasarecutester.com/panda.png)", TextType.TEXT),
                TextNode("A simple text node", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_image_empty_node(self):
        node = TextNode(
            "",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [

            ],
            new_nodes
        )

    def test_split_link_empty_node(self):
        node = TextNode(
            "",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [

            ],
            new_nodes
        )


class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnode(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result_nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
                TextNode('This is ', TextType.TEXT),
                TextNode('text', TextType.BOLD),
                TextNode(' with an ', TextType.TEXT),
                TextNode('italic', TextType.ITALIC),
                TextNode(' word and a ', TextType.TEXT),
                TextNode('code block', TextType.CODE),
                TextNode(' and an ', TextType.TEXT),
                TextNode('obi wan image', TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(' and a ', TextType.TEXT),
                TextNode('link', TextType.LINK, "https://boot.dev") ,
            ],
            result_nodes
        )

    def test_ttt_format_start(self):
        test_text = "**Bold Title** _text with an italic body_ and a lovely simple ending link [anchor](https://www.alabamibuckstep.com)"
        result_nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
                TextNode('Bold Title', TextType.BOLD),
                TextNode(' ', TextType.TEXT),
                TextNode('text with an italic body', TextType.ITALIC),
                TextNode(' and a lovely simple ending link ', TextType.TEXT),
                TextNode('anchor', TextType.LINK, 'https://www.alabamibuckstep.com'),
            ],
            result_nodes
        )

    def test_ttt_format_end(self):
        test_text = "This text contains an image ![marching photo](https://www.alabamibuckstep.com/marchingparade.jpg) _marching photo 2007 parade_"
        result_nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
                TextNode('This text contains an image ', TextType.TEXT),
                TextNode('marching photo', TextType.IMAGE, 'https://www.alabamibuckstep.com/marchingparade.jpg'),
                TextNode(' ', TextType.TEXT),
                TextNode('marching photo 2007 parade', TextType.ITALIC),
            ],
            result_nodes
        )

    def test_ttt_all_urls(self):
        test_text = "[youtube link](https://www.youtube.com)![image](www.image.com)`random code block lol`[image site](www.alinktoimagesite.net/with-a-fun-url) and some text at the end"
        result_nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
                TextNode('youtube link', TextType.LINK, 'https://www.youtube.com'),
                TextNode('image', TextType.IMAGE, 'www.image.com'),
                TextNode('random code block lol', TextType.CODE),
                TextNode('image site', TextType.LINK, 'www.alinktoimagesite.net/with-a-fun-url'),
                TextNode(' and some text at the end', TextType.TEXT),
            ],
            result_nodes
        )

if __name__ == "__main__":
    unittest.main()