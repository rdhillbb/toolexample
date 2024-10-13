import os
import re

def clean_text(text):
    # Unescape Unicode
    text = text.encode().decode('unicode_escape')
    
    # Remove zero-width spaces and other invisible characters
    text = re.sub(r'[\u200b-\u200d\ufeff]', '', text)
    
    # Remove binary codes (assuming they're represented as \x followed by two hex digits)
    text = re.sub(r'\\x[0-9a-fA-F]{2}', '', text)
    
    return text

def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            
            # Read the original file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            # Clean the content
            cleaned_content = clean_text(content)
            
            # Write the cleaned content to a new file
            cleaned_filename = f"cleaned_{filename}"
            cleaned_file_path = os.path.join(directory_path, cleaned_filename)
            with open(cleaned_file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            
            # Rename the original file
            dirty_filename = f"{filename}.dirty"
            dirty_file_path = os.path.join(directory_path, dirty_filename)
            os.rename(file_path, dirty_file_path)
            
            print(f"Processed {filename}")
            print(f"  Created: {cleaned_filename}")
            print(f"  Renamed original to: {dirty_filename}")

# Example usage
directory_to_process = "./TopDrawer"
process_directory(directory_to_process)
