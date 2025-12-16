from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            fatty = node.text.split(delimiter)
            if len(fatty) == 1:
                # print("NO DELIMITER FOUND, KEEPING AS-IS: ", repr(node.text))  # DEBUG print
                new_nodes.append(node)
                continue

            if len(fatty) % 2 == 0:
                # print("BROKEN MARKDOWN IN NODE: ", repr(node.text))   # DEBUG print
                raise Exception("Invalid Markdown: missing delimiter")
            
            # print("SPLITTING NODE: ", repr(node.text), "->", fatty)   # DEBUG print
            for i, chunk in enumerate(fatty):
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
        image_node = extract_markdown_images(node.text)
        if len(image_node) == 0:
            new_nodes.append(node)
        image_alt = image_node[0][0]
        image_link = image_node[0][1]
        fatty = node.text.split(f"![{image_alt}]({image_link})", 1)
        if len(fatty) == 1:
            new_nodes.extend(image_alt, image_link)
            continue
        else:
            new_nodes.extend([image_alt, image_link])
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_node = extract_markdown_links(node.text)
        if len(image_node) == 0:
            new_nodes.append(node)
        image_alt = image_node[0][0]
        image_link = image_node[0][1]
        fatty = node.text.split(f"[{image_alt}]({image_link})", 1)
        if len(fatty) == 1:
            new_nodes.extend(image_alt, image_link)
            continue
        else:
            new_nodes.extend([image_alt, image_link])
            
    return new_nodes



# for node in new_nodes:
#     print(f"TextNode({node.text}, {node.text_type})")
if __name__ == "__main__":
    node = TextNode(
        "This is text with an image link ![boots png](https://www.boot.dev/profile/image/boots_smirk) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    print(split_nodes_image([node]))

    node2 = TextNode(
        "This is text with an image link ![boots png](https://www.boot.dev/profile/image/boots_smirk) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    print(split_nodes_link([node2]))

    node3 = TextNode(
        "This is a text node with __italic block__ see how it shines.",
        TextType.TEXT
    )
    split_del = split_nodes_delimiter([node3], "__", TextType.ITALIC)
    for n in split_del:
        print(n)