import os
import sys
import shutil

from copystatic import copy_directory # type: ignore
from gencontent import generate_pages_recursive # type: ignore


static_path = "./static"
content_path = "./content"
template_path = "./template.html"
public_path = "./public"
docs_path = "./docs"

spacer = "\n- - - - - - - - - -\n"

# used wget -O static/images/tom.png https: //storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/tom.png
# to get images into directory
def main():
    print(spacer + "Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("Copying static files to docs directory...")
    copy_directory(static_path, docs_path)
    print(f"Successfully copied content of {static_path} to {docs_path} !" + spacer)

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"basepath == {basepath}")

    generate_pages_recursive(content_path, template_path, docs_path, basepath)
    print(spacer)


if __name__ == "__main__":
    main()