## Helpers for parsing text into block markdown
import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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
            return BlockType.UNORDERED_LIST
        if smash[0].startswith("1. "):
            i = 1
            for line in smash:
                if not line.startswith(f"{i}. "):
                    return BlockType.PARAGRAPH
                i += 1
            return BlockType.ORDERED_LIST

    else:
        if re.findall(r"^#{1,6}\s", block):
            return BlockType.HEADING
        if len(block) > 3 and block[0:3] == ("```"):
            if re.findall(r"(?<!`)`{3}$", block):
                return BlockType.CODE
        if block.startswith(">"):
            return BlockType.QUOTE
        if block.startswith("- "):
            return BlockType.UNORDERED_LIST
        if block.startswith("1. "):
            return BlockType.ORDERED_LIST
    return block_type



# if __name__ == "__main__":
#     md = """
# > A quote

# - Unordered

# 1. Ordered

# >

# - 

# 1. 
# """

#     result = markdown_to_blocks(md)
#     # print(result)
#     for r in result:
#         # print(f"\nCHECKING TYPE of block:\n{r}")
#         print(f">>> {block_to_block_type(r)} <<<")
    