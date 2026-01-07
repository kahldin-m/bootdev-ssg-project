import os
import shutil

from copystatic import copy_directory # type: ignore
from gencontent import generate_page # type: ignore


static_path = "./static"
public_path = "./public"
index_path = "./content/index.md"
template_path = "./template.html"
index_dest = "./public/index.html"

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

    generate_page(index_path, template_path, index_dest)
    print(spacer)


if __name__ == "__main__":
    main()