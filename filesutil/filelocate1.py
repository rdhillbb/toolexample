import os

# Base path where the top-level directories are located
import re
def list_files_in_level2(uuid, top_directory):
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    top_path = os.path.join(storage,uuid, top_directory)
    print(top_path)
    #result = f"UUID: {uuid}\n"

    result = f"Cabinet  {top_directory}\n"
    # Walk through the directory
    for root, dirs, files in os.walk(top_path):
        level = root.count(os.sep) - top_path.count(os.sep)
       
        # Process Level 1 directories
        if level == 1:
            result += f"*   {os.path.basename(root)}:\n"
        # List files in Level 2 directories
        elif level == 2:
            dir_name = os.path.basename(root)
            result += f"\n      {dir_name}\n"
            for file in files:
                result += f"\t{file}\n"
    return result


def find_fileX(uuid, filename):
    """
    Search for a file with a given name within a specified directory and all its subdirectories.

    Parameters:
    directory (str): The path to the directory where the search should start.
    filename (str): The name of the file to search for.

    Returns:
    str: The path to the file if found, otherwise None.
    """
    searchresults = []
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    directory = os.path.join(storage,uuid,)
    for root, dirs, files in os.walk(directory):
        if filename in files:
            tmp = root
            parts = tmp.split(directory)
            searchresults.append(os.path.join(parts[1], filename))
            #continue
            #return os.path.join(parts[1], filename)  # Return the full path to the file

    return searchresults  # Return None if the file was not found
import os

def find_fileXX(uuid, filename):
    """
    Search for files that match a given name or extension within a specified directory and all its subdirectories.

    Parameters:
    uuid (str): The UUID associated with the directory.
    filename (str): The name of the file or extension to search for.

    Returns:
    list: A list of paths to the files if found, otherwise an empty list.
    """
    search_results = []
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    directory = os.path.join(storage, uuid)

    # Split the input to handle both name and extension separately
    name, ext = os.path.splitext(filename)
    if ext == '':
        # The user provided only a name or only an extension
        name_search = name
        ext_search = name
    else:
        # The user provided a full file name
        name_search = name
        ext_search = ext

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            # Match against both just name, just extension, or full filename
            if file_name == name_search or file_ext == ext_search or file == filename:
                # Construct a relative path from the base directory
                relative_path = os.path.relpath(root, directory)
                search_results.append(os.path.join(relative_path, file))

    return search_results
import subprocess
import os

def find_files_with_find(uuid, search_term):
    """
    Use the Linux `find` command to search files based on name or extension.

    Parameters:
    uuid (str): The UUID associated with the directory.
    search_term (str): The search term, which could be a filename or extension.

    Returns:
    list: A list of paths to the files if found, otherwise an empty list.
    """
    storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    directory = os.path.join(storage, uuid)

    # Handling different types of search inputs
    if '.' in search_term:
        # Assume it's either a full filename or an extension
        search_pattern = f"*{search_term}"
    else:
        # Search for any file having the search_term in its name or as an extension
        search_pattern = f"*{search_term}*.*"

    # Execute the find command
    try:
        result = subprocess.run(
            ["find", directory, "-type", "f", "-name", search_pattern],
            text=True, capture_output=True
        )
        if result.stdout:
            # Split the output into lines to get each path
            return result.stdout.strip().split('\n')
        else:
            return []
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []
import subprocess
import os

def find_files_with_findX(uuid, search_term):
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

# Example usage


# Example usage
print(list_files_in_level2("uuid-1234-1234","MiddleFileCabinet"))
print(find_fileX("uuid-1234-1234","food.pdf"))
#print(find_fileXX("uuid-1234-1234","pdf"))
print(find_files_with_findX("uuid-1234-1234","pdf"))
