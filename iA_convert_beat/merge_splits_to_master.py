import os

def merge_splits_to_master(output_file="master.fountain"):
    """
    Rebuilds the master.fountain file by merging content from a structured folder hierarchy.
    - Acts are top-level folders marked with # (e.g., #Act 1).
    - Scenes are subfolders marked with ## (e.g., ##Opening Image).
    - Beats are files marked with . and their content follows (e.g., .forest).
    - Adds a blank line between Acts, Scenes, and Beats for readability.
    - Removes numbering from folder and file names when writing to the master file.
    """
    base_dir = "split_files"

    if not os.path.exists(base_dir):
        print(f"Directory '{base_dir}' does not exist.")
        return

    # Step 1: Prepare header and footer from the original master file
    header_lines = []
    footer_line = ""
    if os.path.exists(output_file):
        with open(output_file, 'r') as master_file:
            lines = master_file.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("#"):
                    # Stop collecting header when Acts start
                    break
                header_lines.append(line)
            if lines:
                footer_line = lines[-1].strip()

    # Step 2: Traverse the folder structure to build the new content
    new_content = []

    for act_folder in sorted(os.listdir(base_dir)):
        if act_folder.startswith("."):
            # Skip hidden files and folders
            continue

        act_path = os.path.join(base_dir, act_folder)

        if not os.path.isdir(act_path):
            # Skip non-folder entries
            continue

        # Add Act marker, remove numbering
        act_marker = f"#{' '.join(act_folder.split('_')[1:])}"
        new_content.append(act_marker)
        new_content.append("")  # Add blank line after Act marker

        for scene_folder in sorted(os.listdir(act_path)):
            if scene_folder.startswith("."):
                # Skip hidden files and folders
                continue

            scene_path = os.path.join(act_path, scene_folder)

            if not os.path.isdir(scene_path):
                # Skip non-folder entries
                continue

            # Add Scene marker, remove numbering
            scene_marker = f"## {' '.join(scene_folder.split('_')[1:])}"
            new_content.append(scene_marker)
            new_content.append("")  # Add blank line after Scene marker

            for beat_file in sorted(os.listdir(scene_path)):
                if beat_file.startswith("."):
                    # Skip hidden files
                    continue

                beat_path = os.path.join(scene_path, beat_file)

                if not os.path.isfile(beat_path) or not beat_file.endswith(".fountain"):
                    # Skip non-fountain files
                    continue

                # Add Beat marker, remove numbering, and content
                beat_marker = f".{beat_file.split('_', 1)[1].replace('_', ' ').replace('.fountain', '')}"
                new_content.append(beat_marker)

                with open(beat_path, 'r') as beat:
                    beat_content = beat.read().strip()
                    new_content.append(beat_content)
                    new_content.append("")  # Add blank line after Beat content

    # Step 3: Write the new master file
    with open(output_file, 'w') as master_file:
        # Write header lines
        master_file.writelines(header_lines)

        # Write new content
        for line in new_content:
            master_file.write(line + "\n")

        # Write footer line
        if footer_line:
            master_file.write(footer_line + "\n")

    print(f"Merged content written to '{output_file}'.")

# Example usage:
merge_splits_to_master()
