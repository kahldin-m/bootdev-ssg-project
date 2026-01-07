import os
import shutil

from copystatic import copy_directory # type: ignore
from gencontent import generate_pages_recursive # type: ignore


static_path = "./static"
content_path = "./content"
template_path = "./template.html"
public_path = "./public"

spacer = "\n- - - - - - - - - -\n"

# used wget -O static/images/tom.png https: //storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/tom.png
# to get images into directory
def main():
    print(spacer + "Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("Copying static files to public directory...")
    copy_directory(static_path, public_path)
    print(f"Successfully copied content of {static_path} to {public_path} !" + spacer)

    generate_pages_recursive(content_path, template_path, public_path)
    print(spacer)


if __name__ == "__main__":
    main()