import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()