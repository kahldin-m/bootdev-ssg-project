import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_h1_at_bottom(self):
        md = """
Tolkien Fan Club

# The End
"""
        self.assertEqual(extract_title(md), "The End")

    def test_missing_header(self):
        md = "This text lacks a heading\nForever to wander aimlessly"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_faulty_header(self):
        md = "#Header hash is too close!"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()