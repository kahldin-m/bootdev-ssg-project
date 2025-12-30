## Helpers for parsing text into block markdown
import re
from enum import Enum
from textnode import TextNode, text_node_to_html_node, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
import inline_markdown as imd


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    prep_md = [s.strip() for s in markdown.split('\n\n')]
    block_strings = []
    for line in prep_md:
        if line != "":
            block_strings.append(line)

    return block_strings

def block_to_block_type(block):
    smash = block.split("\n")
    block_type = BlockType.PARAGRAPH
    if len(smash) > 1:
        if smash[0] == ("```") and smash[-1] == ("```"):
            return BlockType.CODE
        if smash[0].startswith(">"):
            for line in smash:
                if not line.startswith(">"):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        if smash[0].startswith("- "):
            for line in smash:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.ULIST
        if smash[0].startswith("1. "):
            i = 1
            for line in smash:
                if not line.startswith(f"{i}. "):
                    return BlockType.PARAGRAPH
                i += 1
            return BlockType.OLIST

    else:
        if re.findall(r"^#{1,6}\s", block):
            return BlockType.HEADING
        if len(block) > 3 and block[0:3] == ("```"):
            if re.findall(r"(?<!`)`{3}$", block):
                return BlockType.CODE
        if block.startswith(">"):
            return BlockType.QUOTE
        if block.startswith("- "):
            return BlockType.ULIST
        if block.startswith("1. "):
            return BlockType.OLIST
    return block_type


##  Takes a full markdown document and converts it into a single parent HTMLNode
##  That one parent node should contain many child HTMLNode objects representing
##      the nested elements
def markdown_to_html_node(markdown):
    div_node = ParentNode("div", [], None)
    # Split md into blocks
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        # Determing block type
        typed_block = block_to_block_type(block)
        if typed_block == BlockType.HEADING:
            hashes = 0
            for hash in block:
                if hash == "#":
                    hashes += 1
                else:
                    break
            clean_text = block.strip("#")
            new_block_children = text_to_children(clean_text.strip())
            div_node.children.append(ParentNode(f"h{hashes}", new_block_children, None))
        elif typed_block == BlockType.PARAGRAPH:
            new_block_children = text_to_children(block)
            div_node.children.append(ParentNode("p", new_block_children, None))
        elif typed_block == BlockType.CODE:
            clean_text = block.strip("```")
            clean_text_two = clean_text.rstrip("```")
            code_node = text_node_to_html_node(TextNode(clean_text_two.strip(), TextType.CODE))
            div_node.children.append(ParentNode("pre", [code_node]))
        elif typed_block == BlockType.QUOTE:
            clean_text = block.lstrip(">")
            new_block_children = text_to_children(clean_text)
            div_node.children.append(ParentNode("blockquote", new_block_children, None))
        elif typed_block == BlockType.ULIST:
            clean_text = block.lstrip("-")
            new_block_children = text_to_children(clean_text.strip())
            div_node.children.append(ParentNode("ul", new_block_children, None))
        elif typed_block == BlockType.OLIST:
            clean_text = block.lstrip("0123456789.")
            new_block_children = text_to_children(clean_text.strip())
            div_node.children.append(ParentNode("ol", new_block_children, None))
        else:
            raise Exception("Duh, something went wrong.")
    

    # GOAL: Return an HTMLNode for the whole document: a Parent <div> node whose children
    # are block-level nodes (like <p>, <h1>, <ul>, etc.)
    # Each paragraph block becomes one <p> node whose children are inline LeafNodes
    # created from the paragraph’s text.
    return div_node

### helper functions
def text_to_children(text):
    # Take a string of text and return a list of
    # HTMLNodes that represent the inline markdown
    # using TextNode -> HTMLNode
    print(f">>TEXT to Child == {text} <<<")
    new_texts = imd.text_to_textnodes(text)
    text_nodes = []
    for new in new_texts:
        text_nodes.append(text_node_to_html_node(new))
    return text_nodes


if __name__ == "__main__":
## Block to HTMLNode test
    md = """
### A heading title

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text

```And a code block```

- unordered
- list items
- item third

1. ordered
2. list
3. items

Plus two [link](www.site.com) ![img](www.image.com)

>And a quote from your future self
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)
    

## Block Type test
#     md = """
# > A quote

# - Unordered

# 1. Ordered
# """
#     result = markdown_to_blocks(md)
#     # print(result)
#     for r in result:
#         # print(f"\nCHECKING TYPE of block:\n{r}")
#         print(f">>> {block_to_block_type(r)} <<<")
    