import os

import gitignore_parser


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
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_list.append((file_path, filename))

    return file_list


def filter_files(file: tuple[str, str], is_ignored):
    if is_ignored(file[0]):
        return False
    elif file[0].startswith("./.git"):
        return False
    elif file[0].startswith("./scripts"):
        return False
    elif file[1].endswith("link_all.py"):
        return False
    return True


def create_symlink(target_path, link_name):
    """
    Creates a symbolic link if it doesn't already exist.
    Args:
    - target_path: The file to link to.
    - link_name: The name of the symlink.
    """
    if not os.path.exists(link_name):
        try:
            folder_path = os.path.dirname(link_name)
            os.makedirs(folder_path, exist_ok=True)
            os.symlink(target_path, link_name)
            print(f"Created symlink: {link_name} -> {target_path}")
            return 1
        except OSError as e:
            print(f"Failed to create symlink: {e}")
    return 0


if __name__ == "__main__":
    # Directory to start the search from
    start_directory = "."

    # Check if the directory exists
    if not os.path.exists(start_directory):
        print("Directory not found.")
    else:
        # Parse .gitignore file
        gitignore_path = os.path.join(start_directory, ".gitignore")
        if os.path.exists(gitignore_path):
            is_ignored = gitignore_parser.parse_gitignore(gitignore_path)
        else:
            is_ignored = (
                lambda _: False
            )  # If .gitignore doesn't exist, don't ignore anything

        # Retrieve files
        files = get_files_in_directory(start_directory)
        files = list(filter(lambda file: filter_files(file, is_ignored), files))

        print(len(files))

        # Display files with their paths
        if files:
            count = 0
            for file_path, filename in files:
                target_path = os.path.abspath(file_path)
                link_name = target_path.replace("/dotfiles", "")
                count += create_symlink(target_path, link_name)
            print(f"Linked {count} new files.")
        else:
            print("No files found in the directory and its subdirectories.")
