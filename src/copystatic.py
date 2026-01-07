import os
import shutil


def copy_directory(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f"ERROR: '{src}' directory not found!")  
    # If dst directory does not exist, make one
    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        full_path = os.path.join(src, item)
        # if item is a file, simply copy
        if os.path.isfile(full_path):
            print(f" * static/{item} -> public/{item} (file)")
            shutil.copy(full_path, dst)
        # if the item is a directory, make a copy of that directory by name, then recurse into
        # it to copy whatever files are inside... does that maek sense?
        elif os.path.isdir(full_path):
            new_dst = os.path.join(dst, item)
            print(f" * static/{item} -> public/{item} (dir)")
            copy_directory(full_path, new_dst)

        else:
            raise Exception(f"Something is wrong with item: {item}  :(")