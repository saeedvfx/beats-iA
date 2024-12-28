import os

def prep_splits_for_merge(base_dir="split_files"):
    """
    Prepares split files for merging by:
    - Removing all blank lines between paragraphs in .fountain files.
    - Replacing spaces with underscores in folder and file names.
    
    Args:
        base_dir (str): Path to the base directory containing the split files.
    """
    if not os.path.exists(base_dir):
        print(f"Directory '{base_dir}' does not exist.")
        return

    # Traverse the directory structure
    for root, dirs, files in os.walk(base_dir, topdown=False):
        # Process and clean .fountain files first
        for file_name in files:
            if file_name.endswith(".fountain"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Remove all blank lines
                cleaned_lines = [line for line in lines if line.strip() != ""]

                # Write cleaned content back to the file
                with open(file_path, 'w') as file:
                    file.writelines(cleaned_lines)

        # Rename files in the current directory
        for file_name in files:
            if " " in file_name:
                old_path = os.path.join(root, file_name)
                new_name = file_name.replace(" ", "_")
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

        # Rename directories in the current directory
        for dir_name in dirs:
            if " " in dir_name:
                old_path = os.path.join(root, dir_name)
                new_name = dir_name.replace(" ", "_")
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

    print(f"Prep completed: All blank lines removed and spaces replaced in '{base_dir}'.")

if __name__ == "__main__":
    # Call the function to prep the split files for merging
    prep_splits_for_merge()
