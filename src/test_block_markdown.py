import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType # type: ignore


class TestBlockMardown(unittest.TestCase):

    def test_mardown_to_block(self):
        md = """
This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_whitespace_stripping(self):
        md = """
   A paragraph with 3 leading whitespaces should be stripped clean
with no whitespace left

And a paragraph with whitespace between lines
   like this is unaffected

What about a paragraph with trailing whitespaces 1 2 3   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "A paragraph with 3 leading whitespaces should be stripped clean\nwith no whitespace left",
                "And a paragraph with whitespace between lines\n   like this is unaffected",
                "What about a paragraph with trailing whitespaces 1 2 3",
            ],
        )

    def test_empty_blocks(self):
        md = """
A test of large empty blocks ; they should be removed properly



Like the _ones_ up above
this paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "A test of large empty blocks ; they should be removed properly",
                "Like the _ones_ up above\nthis paragraph",
            ],
        )

    def test_spaces_and_tabs(self):
        md = """
There are tabs in the paragraph below this one



There are spaces in the paragraph below this one

              

- They should
- Not be
- Included
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "There are tabs in the paragraph below this one",
                "There are spaces in the paragraph below this one",
                "- They should\n- Not be\n- Included",
            ],
        )


    ##  >>>>>>>>>>>>>>>>>>>>
    ##  testing block_to_block_type
    ##  <<<<<<<<<<<<<<<<<<<<

    def test_block_to_block_type(self):
        md = "A simple paragraph of text"
        block = block_to_block_type(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )

    def test_btbt_headings(self):
        md = """
#A bad heading paragraph

## A good heading

###### Another good heading

####### A paragraph with too many hashes, followed by one with no text

###  
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            types
        )


    def test_btbt_coding_blocks(self):
        md = """
```A coding block```

```
A multi-line
coding block
```

```An incorrect coding block````

``````

```
```
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.CODE,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.CODE,
            ],
            types
        )

    def test_multi_line_blocks(self):
        md = """
> A good quote would look
> like this

>a bad quote
like this

- Unordered
- Items
- List of

- chaos
reigns
-supreme

-Does
-It
-Float

1. Apple
2. Ball
3. Cat

1. Mosquito
3.  Missing Dot
2. Sadge

- A mixed
2. List
> and quote
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            types
        )

    def test_one_line_lists(self):
        md = """
> A quote

- Unordered

1. Ordered

>  

-  

1.  
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            types
        )

if __name__ == "__main__":
    unittest.main()