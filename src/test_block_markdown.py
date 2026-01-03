import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
) # type: ignore


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
    ##  block_to_block_type tests
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
        block = "```A coding block```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\nA multi-line\ncoding block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```An incorrect coding block````"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "``````"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

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
                BlockType.ULIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.OLIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            types
        )

    def test_one_line_lists(self):
        block = "> A quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- Unordered"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. Ordered"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = ">  "
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "-  "
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1.  "
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)


    ##  >>>>>>>>>>>>>>>>>>>>
    ##  markdown_to_html_node tests
    ##  <<<<<<<<<<<<<<<<<<<<

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- An unordered list
- with items
- another item

1. An ordered list
2. with an item
3. and another
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>An unordered list</li><li>with items</li><li>another item</li></ul><ol><li>An ordered list</li><li>with an item</li><li>and another</li></ol></div>",
        )

    def test_bad_formatting(self):
        # Expect all paragraphs
        md = """
####### Who ordered #7 heading?

```a code block that shouldn't work````

>>Potentially failed blockquote

A paragraph with good `code` but bad *bold*

-Unordered list
-Failed attempt

1. Ordered
2.Failure

1. Attempt 2
3. is no good
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>####### Who ordered #7 heading?</p><p>```a code block that shouldn't work````</p><blockquote>Potentially failed blockquote</blockquote><p>A paragraph with good <code>code</code> but bad *bold*</p><p>-Unordered list -Failed attempt</p><p>1. Ordered 2.Failure</p><p>1. Attempt 2 3. is no good</p></div>",
        )

if __name__ == "__main__":
    unittest.main()