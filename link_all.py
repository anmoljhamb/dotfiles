import os
import subprocess as sp


def get_files_in_directory(directory):
    """
    Recursively retrieves all files in a given directory and its subdirectories.
    Args:
    - directory: The directory to start the search from.
    Returns:
    - A list of tuples containing (file_path, file_name).
    """
    file_list = []

    # Walk through the directory tree
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_list.append((file_path, filename))

    return file_list


def filter_files(file: tuple[str, str]):
    if file[0].startswith("./.git"):
        return False
    elif file[0].startswith("./scripts"):
        return False
    elif file[1].endswith("link_all.py"):
        return False
    return True


if __name__ == "__main__":
    # Directory to start the search from
    start_directory = "."

    # Check if the directory exists
    if not os.path.exists(start_directory):
        print("Directory not found.")
    else:
        # Retrieve files
        files = get_files_in_directory(start_directory)
        files = list(filter(filter_files, files))

        # Display files with their paths
        if files:
            print("Files found:")
            for file_path, filename in files:
                target_path = os.path.abspath(file_path)
                link_name = target_path.replace("/dotfiles", "")
                cmd = f"> ln -s {target_path} {link_name}"
                print(cmd)
                sp.Popen(["ln", "-s", target_path, link_name])
        else:
            print("No files found in the directory and its subdirectories.")
