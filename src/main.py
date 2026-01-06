import os
from shutil import copy, rmtree
from textnode import TextNode, TextType # type: ignore


def main():
    copy_directory("static", "public")
    print("Successfully copied from '/static' to '/public'")
    # test_node = TextNode("Hello, World!", TextType.BOLD, "https://www.google.com")
    # print(repr(test_node))

def extract_title(markdown):
    pass

def copy_directory(src, dst):
    debug = True
    # first check if the directories exist
    if not os.path.exists(dst):
        raise FileNotFoundError(f"ERROR: '{dst}' directory not found!")
    if not os.path.exists(src):
        raise FileNotFoundError(f"ERROR: '{src}' directory not found!")
    
    # next, delete contents of public to ensure clean copying
    # we will remove the entire public/ tree for now
    # -- all files should already live in static anyway... right?
    if debug:
        print(f"=====START for {src}=====")
        print(f"Removing directory '/{dst}'")
    rmtree(dst)
    if debug:
        print(f"'{dst}' exists == {os.path.exists(dst)}")
        print(f"Making new '/{dst}' directory")

    # now make a new 'dst' dir and copy the contents of 'src' into that
    os.mkdir(dst)
    if debug:
        print(f"'{dst}' exists == {os.path.exists(dst)}")
        print("\n>>COPYING<<")
        print(f"Source files to copy: {os.listdir(src)}")

    for item in os.listdir(src):
        full_path = os.path.join(src, item)
        if debug:
            print(f"'{item}' is item? ({os.path.isfile(full_path)})  is dir? ({os.path.isdir(full_path)})")
        # if item is a file, simply copy
        if os.path.isfile(full_path):
            if debug:
                print(f"Copying item 'root/{src}/{item}' to 'root/{dst}'")
            copy(full_path, dst)
        # if the item is a directory, make a copy of that directory by name, then recurse into
        # it to copy whatever files are inside... does that maek sense?
        elif os.path.isdir(full_path):
            if debug:
                print(f"Copying dir 'root/{src}/{item}' to 'root/{dst}'")
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            if debug:
                print(f"\n>>>STARTING RECURSION into {full_path}<<<\n")
            copy_directory(full_path, new_dst)

        else:
            print(f"Something is wrong with item {item}  :(")
    if debug:
        print(f"=====END for {dst}=====\n")

if __name__ == "__main__":
    main()