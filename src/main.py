from textnode import TextNode, TextType # type: ignore


def main():
    test_node = TextNode("Hello, World!", TextType.BOLD, "https://www.google.com")
    print(repr(test_node))


if __name__ == "__main__":
    main()