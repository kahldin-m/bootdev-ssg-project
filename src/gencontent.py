import os

from block_markdown import markdown_to_html_node



def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Title Extraction Failed! No h1 header line detected!")


def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"File path to {from_path} does not exist!")
    if not os.path.exists(template_path):
        raise Exception(f"File path to {template_path} does not exist!")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path} ...\n")
    with open(from_path) as f:
        # Markdown file
        md_content = f.read()
    with open(template_path) as t:
        # Template file
        html_page = t.read()
    
    # Convert the md_content into an HTML string
    main_content = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    # Replace the placeholder title and content with our own
    html_page = html_page.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", main_content)

    # Create any necessary directories if they don't exist
    dir_dest_path = os.path.dirname(dest_path)
    if dir_dest_path:
        print(f"Creating destination path: {dir_dest_path} ...\n")
        os.makedirs(dir_dest_path, exist_ok=True)

    # Now write a new full HTML page to a file at dest_path
    with open(dest_path, "w") as index_html:
        index_html.write(html_page)

    print(f" *===== Wrote : =====*\n{html_page}\n\n *===== to {dest_path} =====*")
