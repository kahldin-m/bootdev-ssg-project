## Helpers for parsing text into block markdown
import re

from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node

import inline_markdown as imd


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    ## Gotta normalize whitespace to avoice lines with accidental space/tabs
    ## from counting and messing up formatting
    normalized_lines = []
    for line in markdown.split("\n"):
        if line.strip() == "":
            normalized_lines.append("")
        else:
            normalized_lines.append(line)

    normalized = "\n".join(normalized_lines)

    ## Now split into blocks
    blocks = [b.strip() for b in normalized.split("\n\n")]

    ## Filter out empty blocks
    return [b for b in blocks if b != ""]
    # prep_md = [s.strip() for s in markdown.split('\n\n')]
    # block_strings = []
    # for line in prep_md:
    #     if line != "":
    #         block_strings.append(line)

    # return block_strings

def block_to_block_type(block):
    smash = block.split("\n")
    if re.findall(r"^#{1,6}\s", block):
            return BlockType.HEADING
    if len(smash) > 1 and smash[0].startswith("```") and smash[-1].startswith("```"):
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
    return BlockType.PARAGRAPH
    # else:
    #     # if len(block) > 3 and block[0:3] == ("```"):
    #     #     if re.findall(r"(?<!`)`{3}$", block):
    #     #         return BlockType.CODE
    #     if block.startswith(">"):
    #         return BlockType.QUOTE
    #     if block.startswith("- "):
    #         return BlockType.ULIST
    #     if block.startswith("1. "):
    #         return BlockType.OLIST
    


##  Takes a full markdown document and converts it into a single parent HTMLNode
##  That one parent node should contain many child HTMLNode objects representing
##      the nested elements
def markdown_to_html_node(markdown):
    div_node = ParentNode("div", [], None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        try:
            # Determing block type
            typed_block = block_to_block_type(block)
            if typed_block == BlockType.HEADING:
                hashes = 0
                for hasher in block:
                    if hasher == "#":
                        hashes += 1
                    else:
                        break
                clean_text = block.lstrip("#")
                new_block_children = text_to_children(clean_text.strip())
                div_node.children.append(ParentNode(f"h{hashes}", new_block_children, None))

            elif typed_block == BlockType.PARAGRAPH:
                lines = block.split("\n")
                cleaned_lines = []
                for line in lines:
                    cleaned_lines.append(line.strip())
                joined = " ".join(cleaned_lines)
                new_block_children = text_to_children(joined)
                div_node.children.append(ParentNode("p", new_block_children, None))

            elif typed_block == BlockType.CODE:
                div_node.children.append(ParentNode("pre", [code_to_html(block)]))

            elif typed_block == BlockType.QUOTE:
                div_node.children.append(ParentNode("blockquote", quote_to_html(block), None))

            elif typed_block == BlockType.ULIST:
                div_node.children.append(ParentNode("ul", ulist_to_html(block), None))

            elif typed_block == BlockType.OLIST:
                div_node.children.append(ParentNode("ol", olist_to_html(block), None))
            else:
                raise Exception("Duh, something went wrong.")
        except Exception:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.strip())
            joined = " ".join(cleaned_lines)
            text_children = text_node_to_html_node(TextNode(joined, TextType.TEXT))
            div_node.children.append(ParentNode("p", [text_children], None))
    

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
    # print(f">>TEXT to Child == {text} <<<")
    new_texts = imd.text_to_textnodes(text)
    text_nodes = []
    for new in new_texts:
        text_nodes.append(text_node_to_html_node(new))
    return text_nodes

def code_to_html(block):
    block = block[3:-3]
    if block.startswith("\n"):
        block = block[1:]
    lines = block.split("\n")
    code_text = "\n".join(lines)
    code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return code_node

def quote_to_html(block):
    lines = block.split("\n")
    quote_items = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError(">>Invalid Quote block<<")
        quote_items.append(line.lstrip(">").strip())
    result = " ".join(quote_items)
    return text_to_children(result)

def ulist_to_html(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        children = text_to_children(line[2:])
        list_items.append(ParentNode("li", children))
    return list_items

def olist_to_html(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        children = text_to_children(line[3:])
        list_items.append(ParentNode("li", children))
    return list_items


# if __name__ == "__main__":
#     md = """
# # Some heading text in h1

# Normal paragraph
# with multiple
# lines

# ## h2 text here
    
# - list items
# - of unordered

# 1. Ordered List
# 2. Item 2

# > A quote
# > from some
# > guy probably

# ### h3 text here

# A normal paragraph here

# ```
# A block of code
# with **bold**
# and _italic_ inside
# ```

# A paragraph with inline `code` and **bold** and _italic_

# A Paragraph with inline *bold* that is not correct too
# """

#     node = markdown_to_html_node(md)
#     html = node.to_html()
#     print(html)
    