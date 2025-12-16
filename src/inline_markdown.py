import re

def extract_markdown_images(text):
    # From raw markdown text, return a list of tuples. Should contain alt text and URL of markdown images
    return  list(re.findall(r"!\[([^\[\]]*)\].*?\(([^\(\)]*)\)", text))

def extract_markdown_links(text):
    return list(re.findall(r"(?<!!)\[([^\[\]]*)\].*?\(([^\(\)]*)\)", text))



if __name__ == "__main__":
    # text = sys.argv[1] if sys.argv[1] else "No text file provided"
    text_img = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"

    text_link = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    images = extract_markdown_images(text_img)
    links = extract_markdown_links(text_link)
    print(images)
    print(links)