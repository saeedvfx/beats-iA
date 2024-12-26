import os

def replace_underscores_in_names(base_dir):
    """
    Replaces underscores with spaces in folder and file names within the specified base directory.
    
    Args:
        base_dir (str): Path to the base directory containing the split files.
    """
    for root, dirs, files in os.walk(base_dir, topdown=False):
        # Rename files in the current directory
        for file_name in files:
            if "_" in file_name:
                old_path = os.path.join(root, file_name)
                new_name = file_name.replace("_", " ")
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

        # Rename directories in the current directory
        for dir_name in dirs:
            if "_" in dir_name:
                old_path = os.path.join(root, dir_name)
                new_name = dir_name.replace("_", " ")
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

def add_blank_lines_to_paragraphs(base_dir):
    """
    Adds an extra blank line between paragraphs in all .fountain files within the specified base directory.

    Args:
        base_dir (str): Path to the base directory containing the split files.
    """
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.endswith(".fountain"):
                file_path = os.path.join(root, file_name)

                # Read the file content
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Process the lines to add blank lines between paragraphs
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    # If the current line is not empty and the next line exists and is not empty, add a blank line
                    if line.strip() and i + 1 < len(lines) and lines[i + 1].strip():
                        new_lines.append("\n")

                # Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.writelines(new_lines)

def shorten_folder_numbers(base_dir):
    """
    Renames folders by converting the 4-digit number prefix into the first two digits only.

    Args:
        base_dir (str): Path to the base directory containing the split files.
    """
    for root, dirs, _ in os.walk(base_dir, topdown=False):
        for dir_name in dirs:
            parts = dir_name.split(" ", 1)
            if len(parts) > 1 and parts[0].isdigit() and len(parts[0]) == 4:
                old_path = os.path.join(root, dir_name)
                new_name = f"{parts[0][:2]} {parts[1]}"
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

if __name__ == "__main__":
    # Define the base directory for the split files
    split_files_dir = "split_files"

    # Replace underscores with spaces in folder and file names
    replace_underscores_in_names(split_files_dir)

    # Add blank lines between paragraphs in .fountain files
    add_blank_lines_to_paragraphs(split_files_dir)

    # Shorten folder numbers
    shorten_folder_numbers(split_files_dir)

    print("Processing complete: underscores replaced, blank lines added, and folder numbers shortened.")
