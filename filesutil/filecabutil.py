import os



def list_directories_in_cabinet(uuid: str, file_cabinet: str = "MiddleFileCabinet") -> str:
    """
    Lists all directories within a specified cabinet of a user-specific subdirectory located within a given file cabinet.

    Args:
        uuid (str): The UUID representing the user's directory.
        file_cabinet (str): The cabinet name within the user's directory, defaulting to 'MiddleFileCabinet'.

    Raises:
        ValueError: If the UUID or file cabinet path is not set or invalid.
        FileNotFoundError: If the directory does not exist.

    Returns:
        str: A newline-separated list of directory paths within the specified file cabinet.
    """
          # Getting the directory from the environment variable 'GEPPETTO_FILE_CABINET'
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    # If directory path is None
    if storage is None:
         raise ValueError(
             "The environment variable 'GEPPETTO_FILE_CABINET' is not set."
        )

    if not uuid:
        raise ValueError("The UUID is not set or is invalid.")

    if not file_cabinet:
        raise ValueError("The file cabinet path is not set or is invalid.")

    user_directory = os.path.join(storage, uuid, file_cabinet)
    if not os.path.exists(user_directory):
        raise FileNotFoundError(f"The directory {user_directory} does not exist.")
    directories = [os.path.basename(d) for d in os.listdir(user_directory) if os.path.isdir(os.path.join(user_directory, d))]
    if not directories:
        return "No directories found in the specified file cabinet."

    header = f"{file_cabinet.replace('FileCabinet', ' File Cabinet')}\n"  # Beautifies the header name
    return header + "\n".join(directories)+"\n"  # Formats the output to only show directory names

    directories = [os.path.join(user_directory, d) for d in os.listdir(user_directory) if os.path.isdir(os.path.join(user_directory, d))]
    if not directories:
        return "No directories found in the specified file cabinet."

    return "\n".join(f"Directory: {directory}" for directory in directories)
import os
import os

def list_subdirectories_two_levels_deep(uuid: str, file_cabinet: str = "MiddleFileCabinet") -> str:
    """
    Lists directories that are two levels deep relative to the directories found within a specified cabinet
    of a user-specific subdirectory located within a given file cabinet.

    Args:
        uuid (str): The UUID representing the user's directory.
        file_cabinet (str): The cabinet name within the user's directory, defaulting to 'MiddleFileCabinet'.

    Raises:
        ValueError: If the UUID or file cabinet path is not set or invalid.
        FileNotFoundError: If the directory does not exist.

    Returns:
        str: A newline-separated list of directory paths two levels below each directory in the specified file cabinet.
    """
    if not uuid:
        raise ValueError("The UUID is not set or is invalid.")
    if not file_cabinet:
        raise ValueError("The file cabinet path is not set or is invalid.")
          # Getting the directory from the environment variable 'GEPPETTO_FILE_CABINET'
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    # If directory path is None
    if storage is None:
         raise ValueError(
             "The environment variable 'GEPPETTO_FILE_CABINET' is not set."
        )


    base_directory = os.path.join(storage, uuid, file_cabinet)
    if not os.path.exists(base_directory):
        raise FileNotFoundError(f"The directory {base_directory} does not exist.")

    subdirectory_paths = []
    listdir = ""
    first_level_dirs = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    for dir in first_level_dirs:
        #print("DIR",dir)
        drw = header = f"{dir.replace('Drawer', ' Drawer')}\n" 
        listdir +=os.path.basename(os.path.normpath(drw))
        second_level_dirs = [os.path.join(dir, sd) for sd in os.listdir(dir) if os.path.isdir(os.path.join(dir, sd))]
        #print(second_level_dirs)
        for subdir in second_level_dirs:
            listdir +=" ** "+os.path.basename(os.path.normpath(subdir))+"\n"
            #third_level_dirs = [os.path.join(subdir, td) for td in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, td))]
            #subdirectory_paths.extend(third_level_dirs)
        listdir +="\n"

    if not listdir:
        return "No directories found two levels below in the specified file cabinet."

    return listdir
    return "\n".join(f"Directory: {path}" for path in subdirectory_paths)

def list_files_in_level2(uuid, top_directory):
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    top_path = os.path.join(storage,uuid, top_directory)
    #print(top_path)
    #result = f"UUID: {uuid}\n"

    result = f"Cabinet  {top_directory}"
    # Walk through the directory
    for root, dirs, files in os.walk(top_path):
        level = root.count(os.sep) - top_path.count(os.sep)

        # Process Level 1 directories
        if level == 1:
            result += f"*   {os.path.basename(root)}:"
        # List files in Level 2 directories
        elif level == 2:
            dir_name = os.path.basename(root)
            result += f"\n      {dir_name}\n"
            for file in files:
                   result += f"\t{file}\n"
    return result

def find_files_with_find(uuid, search_term):
    """
    Use the Linux `find` command to search for files based on name or extension.

    Parameters:
    uuid (str): The UUID associated with the directory.
    search_term (str): The search term, which could be a filename or extension.

    Returns:
    list: A list of paths to the files if found, otherwise an empty list.
    """
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    directory = os.path.join(storage, uuid)
    stripdir = []
    # Determine the appropriate search pattern based on the input format
    if search_term.startswith('.'):
        # Explicit extension provided (e.g., ".pdf")
        search_pattern = f"*{search_term}"
    elif '.' in search_term:
        # Full filename with extension provided (e.g., "filename.pdf")
        search_pattern = search_term
    else:
        # Only filename or extension without dot provided (e.g., "pdf" or "filename")
        # Search for files with this term as part of their name or as an extension
        search_pattern = f"*{search_term}*"

    # Execute the find command
    try:
        result = subprocess.run(
            ["find", directory, "-type", "f", "-name", search_pattern],
            text=True, capture_output=True
        )
        if result.stdout:
            # Split the output into lines to get each path
            tmp = result.stdout.strip().split('\n')
            for d in tmp:
                stripdir.append(d.split(directory)[1])
            return stripdir
            return tmp.stdout.strip().split(directory)
        else:
            return []
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []
