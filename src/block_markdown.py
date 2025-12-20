## Helpers for parsing text into block markdown
import re
from enum import Enum
from textnode import TextNode, text_node_to_html_node
import inline_markdown as im


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
    # Split md into blocks
    blocks = markdown_to_blocks(markdown)

    # Loop over each block
    block_types = []

    for block in blocks:
        # Determing block type
        fix_nodes = text_to_children(block)
        block_types.append(block_to_block_type(fix_nodes))
        
    return block_types

## helper function
def text_to_children(text):
    print(f"text {text} -> {type(text)}")
    text_nodes = im.text_to_textnodes(text)
    print(f"text {text_nodes} -> {type(text_nodes)}")
    for node in text_nodes:
        new_node = text_node_to_html_node(node)
        print(new_node)




if __name__ == "__main__":
## Block to HTMLNode test
    md = """
# A heading title

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    blocks = markdown_to_html_node(md)
    for block in blocks:
        print(block)

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
    