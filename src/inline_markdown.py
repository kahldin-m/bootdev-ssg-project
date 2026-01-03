#
# >>>>> Helpers for parsing *inline* markdown: bold, italic, code, links, images <<<<<
#
import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    # From raw markdown text, return a list of tuples. Should contain alt text and URL of markdown images
    return  list(re.findall(r"!\[([^\[\]]*)\].*?\(([^\(\)]*)\)", text))

def extract_markdown_links(text):
    return list(re.findall(r"(?<!!)\[([^\[\]]*)\].*?\(([^\(\)]*)\)", text))

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        else:
            fatty = old_node.text.split(delimiter)
            if len(fatty) == 1:
                # print("NO DELIMITER FOUND, KEEPING AS-IS: ", repr(node.text))  # DEBUG print
                new_nodes.append(old_node)
                continue
            if len(fatty) % 2 == 0:
                ## MESSY. DIDN'T KNOW HOW TO HANDLE THIS, BUT WAS CONVINCED TO USE THE EXCEPTION
                ## RATHER THAN ADD IT AS A PLAIN TEXT SEGMENT
                # print("BROKEN MARKDOWN IN NODE: ", repr(node.text))   # DEBUG print
                raise Exception("Invalid Markdown: missing delimiter")
                # new_nodes.append(old_node)
                # continue
            
            # print("SPLITTING NODE: ", repr(node.text), "->", fatty)   # DEBUG print
            for i, chunk in enumerate(fatty):
                if chunk == "":
                    continue
                if i % 2 == 1:
                    new_nodes.append(TextNode(chunk, text_type))
                else:
                    new_nodes.append(TextNode(chunk, TextType.TEXT))
            
    return new_nodes

## Example usage:
# node = TextNode("This is a plain delimiter-less node", TextType.TEXT)
# node2 = TextNode("**This is a bold text only node**", TextType.BOLD)
# node3 = TextNode("This is a text with a `code block` word", TextType.TEXT)
# node4 = TextNode("This is a text with a `code block` and another `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node, node2, node3, node4], '`', TextType.CODE)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        images = extract_markdown_images(current_text)
        if len(images) == 0:
            if node.text != "":
                new_nodes.append(node)
            continue
        for image_alt, image_link in images:
            # print(f"THIS IS IMAGE: {image_alt} <<>> {image_link}")    # DEBUG print
            before, after = current_text.split(f"![{image_alt}]({image_link})", 1)
            # print(f"THIS IS FATTY: {before} <<>> {after}")    # DEBUG print
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = after

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        links = extract_markdown_links(current_text)
        if len(links) == 0:
            if node.text != "":
                new_nodes.append(node)
            continue
        for link_anchor, link_url in links:
            before, after = current_text.split(f"[{link_anchor}]({link_url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            current_text = after
        
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    the_node = [TextNode(text, TextType.TEXT)]
    delimiter_types = [
        ("**", TextType.BOLD), 
        ("_", TextType.ITALIC), 
        ("`", TextType.CODE)
    ]
    for delimiter, tt in delimiter_types:
        the_node = split_nodes_delimiter(the_node, delimiter, tt)
    the_node = split_nodes_image(the_node)
    the_node = split_nodes_link(the_node)
    return the_node

## MANUAL TESTS
# if __name__ == "__main__":
#     node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#     result = text_to_textnodes(node)
#     for line in result:
#         print(line)


#     # text = sys.argv[1] if sys.argv[1] else "No text file provided"
#     text_img = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"

#     text_link = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#     images = extract_markdown_images(text_img)
#     links = extract_markdown_links(text_link)
#     print(images)
#     print(links)

#     node = TextNode(
#         "This is text with an image link ![boots png](https://www.boot.dev/profile/image/boots_smirk) and a link [to youtube](https://www.youtube.com/@bootdotdev) and another image ![image text](https://www.fakeimagesite.com/my_image)",
#         TextType.TEXT,
#     )
#     split_node = split_nodes_image([node])
#     print("Splitting images . . .")
#     for n in split_node:
#         print(n)

#     node2 = TextNode(
#         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and an ![random image](https://cdn.Ppixabay.com/photo/2016/09/16/14/10/mask-1674106_1280.jpg)",
#         TextType.TEXT,
#     )
#     split_node2 = split_nodes_link([node2])
#     print("Splitting links . . .")
#     for n in split_node2:
#         print(n)

    # node3 = TextNode(
    #     "This is a text node with __italic block__ see how it shines.",
    #     TextType.TEXT
    # )
    # split_del = split_nodes_delimiter([node3], "__", TextType.ITALIC)
    # for n in split_del:
    #     print(n)