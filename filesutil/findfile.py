import os
import fnmatch
import json

def find_files(directory, pattern):
    """
    Find files in the given directory and its subdirectories that match the specified pattern.
    
    Args:
    directory (str): The root directory to start the search from.
    pattern (str): The filename pattern to match. Can be a full filename or contain wildcards.
    
    Returns:
    list: A list of dictionaries, each containing 'filepath' and 'filename' for each matching file.
    """
    matches = []
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            filepath = os.path.join(root, filename)
            matches.append({
                "filepath": filepath,
                "filename": filename
            })
    return matches

# Example Usage
if __name__ == "__main__":
    directory = '/home/randolph'
    
    # Test with different patterns
    patterns = ['*.pdf', '*.txt', '*.jpg', 'doc*.docx','*webm']
    
    for pattern in patterns:
        print(f"\nSearching for files matching '{pattern}':")
        found_files = find_files(directory, pattern)
        
        if found_files:
            # Print the results as formatted JSON
            print(json.dumps(found_files, indent=2))
            print(f"Total files found: {len(found_files)}")
        else:
            print(f"No files matching '{pattern}' found in the specified directory and its subdirectories.")

    # Example of how to use the function and work with the results
    pdf_files = find_files(directory, '*.pdf')
    if pdf_files:
        print("\nExample of working with the results:")
        for file_info in pdf_files[:3]:  # Display info for up to 3 files
            print(f"Filename: {file_info['filename']}")
            print(f"Full path: {file_info['filepath']}")
            print()
