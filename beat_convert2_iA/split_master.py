import os
import shutil

def split_into_act_scene_beats():
    """
    Reads master.fountain in the same directory and splits it into a hierarchy of:
      Acts (#) -> Scenes (##) -> Beats (.)
    The last line is removed if it starts with '/*'.
    Unused folders/files in the output directory are removed.
    """

    file_path = "master.fountain"
    output_dir = "split_files"

    # Debug
    print(f"Looking for '{file_path}' in {os.getcwd()}")

    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found in the current directory.")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Remove the last line if it starts with '/*'
    if lines and lines[-1].startswith("/*"):
        print("Debug: Removing last line because it starts with '/*'")
        lines = lines[:-1]

    # We'll parse the lines into data structures, then write them to disk.
    # Structure outline:
    #
    # acts = [
    #   {
    #     "name": "Act1",
    #     "scenes": [
    #       {
    #         "name": "Scene1",
    #         "beats": [
    #           {
    #             "name": "Beat1",
    #             "content": ["Line1\n", "Line2\n", ...]
    #           },
    #           ...
    #         ]
    #       },
    #       ...
    #     ]
    #   },
    #   ...
    # ]

    acts = []
    current_act = None
    current_scene = None
    current_beat = None
    current_beat_content = []

    def finalize_beat():
        """Finalize the current beat (if any) into current_scene['beats'], reset local beat variables."""
        nonlocal current_beat, current_beat_content
        if current_beat and current_scene:
            current_scene["beats"].append({
                "name": current_beat,
                "content": current_beat_content
            })
        current_beat = None
        current_beat_content = []

    def finalize_scene():
        """Finalize the current scene (if any) into current_act['scenes'], reset local scene variables."""
        nonlocal current_scene
        if current_scene and current_act:
            finalize_beat()
            current_act["scenes"].append(current_scene)
        current_scene = None

    def finalize_act():
        """Finalize the current act (if any) into acts, reset local act variable."""
        nonlocal current_act
        if current_act:
            finalize_scene()
            acts.append(current_act)
        current_act = None

    # Parse the lines to fill our structure
    for line in lines:
        stripped = line.strip()

        # --- Check for Act markers (#) ---
        if stripped.startswith("#") and not stripped.startswith("##"):
            # Finalize the previous act
            finalize_act()
            # Create a new act
            act_name = stripped.lstrip('#').strip().replace(" ", "_")
            current_act = {
                "name": act_name,
                "scenes": []
            }

        # --- Check for Scene markers (##) ---
        elif stripped.startswith("##"):
            # Finalize the previous scene
            finalize_scene()
            # Create a new scene
            scene_name = stripped.lstrip('#').strip().replace(" ", "_")
            current_scene = {
                "name": scene_name,
                "beats": []
            }

        # --- Check for Beat markers (.) ---
        elif stripped.startswith("."):
            # Finalize the previous beat
            finalize_beat()
            # Start a new beat
            beat_name = stripped.lstrip('.').strip().replace(" ", "_")
            current_beat = beat_name
            current_beat_content = []

        else:
            # If we're in a beat, add content to that beat
            if current_beat is not None:
                current_beat_content.append(line)
            # Otherwise, ignore lines that don't belong to a beat yet.

    # Finalize any open act/scene/beat
    finalize_act()

    # Debug prints: how many acts, scenes, and beats were parsed
    print(f"Parsed {len(acts)} act(s) total.")
    for i, act_data in enumerate(acts, start=1):
        print(f"  Act {i} [{act_data['name']}] has {len(act_data['scenes'])} scene(s).")

    # Now write everything to disk
    used_paths = set()

    for act_index, act_data in enumerate(acts, start=1):
        # e.g. 01_ActOne
        act_folder_name = f"{act_index:02d}_{act_data['name']}"
        act_folder_path = os.path.join(output_dir, act_folder_name)
        os.makedirs(act_folder_path, exist_ok=True)
        used_paths.add(act_folder_path)

        for scene_index, scene_data in enumerate(act_data["scenes"], start=1):
            # e.g. 01_SceneOne
            scene_folder_name = f"{scene_index:02d}_{scene_data['name']}"
            scene_folder_path = os.path.join(act_folder_path, scene_folder_name)
            os.makedirs(scene_folder_path, exist_ok=True)
            used_paths.add(scene_folder_path)

            for beat_index, beat_data in enumerate(scene_data["beats"], start=1):
                # e.g. 01_BeatOne.fountain
                beat_file_name = f"{beat_index:02d}_{beat_data['name']}.fountain"
                beat_file_path = os.path.join(scene_folder_path, beat_file_name)

                with open(beat_file_path, 'w', encoding='utf-8') as bf:
                    bf.writelines(beat_data["content"])

                used_paths.add(beat_file_path)

    # Cleanup anything not used
    cleanup_unused(output_dir, used_paths)
    print("Done! Check the 'split_files' folder.")


def cleanup_unused(parent_path, used_paths):
    """
    Deletes files and folders in the parent path that are not in the used_paths set.
    Recursively walks subdirectories to remove unused items.
    """
    for item in os.listdir(parent_path):
        item_path = os.path.join(parent_path, item)
        if os.path.isdir(item_path):
            # Recursively clean up subdirectories first
            cleanup_unused(item_path, used_paths)
            if item_path not in used_paths and os.path.exists(item_path):
                shutil.rmtree(item_path)
        else:
            if item_path not in used_paths and os.path.exists(item_path):
                os.remove(item_path)

# If this file is run directly, automatically split master.fountain
if __name__ == "__main__":
    split_into_act_scene_beats()