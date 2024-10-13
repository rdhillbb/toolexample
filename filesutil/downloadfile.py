import os
import chardet

def is_garbled(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read(1024)  # Read the first 1K bytes
        
        # Detect encoding
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        
        if encoding is None:
            return True  # If encoding can't be detected, it's likely garbled
        
        # Attempt to decode using detected encoding
        try:
            decoded_data = raw_data.decode(encoding)
        except UnicodeDecodeError:
            return True  # If decoding fails, it's likely garbled
        
        # Check for non-printable characters
        printable = set(chr(i) for i in range(32, 127)) | {'\t', '\n', '\r'}
        if any(char not in printable for char in decoded_data if char not in '\t\n\r'):
            return True
        
        return False
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return True

def process_file(file_path):
    if not (file_path.endswith('.html') or file_path.endswith('.txt') or file_path.endswith('.md')):
        print(f"Skipping non-HTML/TXT/MD file: {file_path}")
        return False

    print(f"Processing file: {file_path}")
    if is_garbled(file_path):
        print(f"The file {file_path} contains garbled text.")
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False
    else:
        print(f"The file {file_path} is free of garbled text.")
        return False

def check_and_delete_garbled_text_in_directory(directory_path):
    deleted_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if process_file(file_path):
                deleted_files.append(file_path)
    
    return deleted_files

if __name__ == "__main__":
    directory_path = input("Enter the directory path: ")
    deleted_files = check_and_delete_garbled_text_in_directory(directory_path)
    
    print("\nSummary:")
    print(f"Total files deleted: {len(deleted_files)}")
    if deleted_files:
        print("Deleted files:")
        for file in deleted_files:
            print(file)
