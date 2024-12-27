import os
import shutil

def split_master_fountain(file_path):
    """
    Splits a master.fountain file into folders and files based on markers:
    - Double-hash markers (##) define sections, converted to folders.
    - Single-line markers starting with a period (.) define beats, converted to files.
    - Lines starting with a single # (e.g., #Act2) are ignored.
    - Removes the last line if it starts with '/*'.
    Cleans up unused folders and files.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove the last line if it starts with '/*'
    if lines and lines[-1].startswith("/*"):
        lines = lines[:-1]

    section_number = 100  # Starting number for sections (incremented by 100)
    section_name = None
    section_content = []
    output_dir = "split_files"

    # Track used folders
    used_folders = set()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Skip lines until the first section marker is found
    found_first_section = False

    for line in lines:
        # Ignore single hash lines (e.g., #Act2)
        if line.startswith("#") and not line.startswith("##"):
            continue

        # Check for section markers (##)
        if line.startswith("##"):
            found_first_section = True

            # Save the previous section if one exists
            if section_name:
                folder_path = save_section(section_name, section_number, section_content, output_dir)
                used_folders.add(folder_path)  # Track used folder
                section_content = []  # Reset for the next section
                section_number += 100  # Increment section number

            # Extract section name, remove the "##" marker, and replace spaces with underscores
            section_name = line.strip().lstrip("#").strip().replace(" ", "_")

        elif found_first_section:
            # Append lines to the current section content
            section_content.append(line)

    # Save the last section
    if section_name:
        folder_path = save_section(section_name, section_number, section_content, output_dir)
        used_folders.add(folder_path)

    # Cleanup unused folders
    cleanup_unused(output_dir, used_folders)


def save_section(name, number, content, output_dir):
    """
    Saves a section to a folder and splits its beats into separate files.
    Cleans up unused files in the folder.
    """
    folder_name = f"{number:04d}_{name}"
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    beat_number = 1
    beat_content = []
    beat_name = None

    # Track used files
    used_files = set()

    for line in content:
        if line.startswith("."):
            # Save the previous beat if one exists
            if beat_name:
                file_path = save_beat(folder_path, beat_name, beat_number, beat_content)
                used_files.add(file_path)  # Track used file
                beat_content = []  # Reset for the next beat
                beat_number += 1  # Increment beat number

            # Extract beat name, remove the "." marker, and replace spaces with underscores
            beat_name = line.strip().lstrip(".").strip().replace(" ", "_")
        else:
            # Append lines to the current beat content
            beat_content.append(line)

    # Save the last beat
    if beat_name:
        file_path = save_beat(folder_path, beat_name, beat_number, beat_content)
        used_files.add(file_path)

    # Cleanup unused files
    cleanup_unused(folder_path, used_files)

    return folder_path


def save_beat(folder_path, name, number, content):
    """
    Saves a beat as a numbered file in the specified folder.
    """
    file_name = f"{number:02d}_{name}.fountain"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        file.writelines(content)
    return file_path


def cleanup_unused(parent_path, used_paths):
    """
    Deletes files and folders in the parent path that are not in the used paths.
    """
    for item in os.listdir(parent_path):
        item_path = os.path.join(parent_path, item)
        if item_path not in used_paths:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Delete unused folder
            else:
                os.remove(item_path)  # Delete unused file


# Example usage:
# Replace 'master.fountain' with the path to your input file.
split_master_fountain("master.fountain")