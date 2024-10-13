import uuid
import os
import requests
from urllib.parse import urlparse
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_top_drawer_path(uuid_str):
    file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
    if not file_cabinet_path:
        raise EnvironmentError("GOVBOTIC_FILE_CABINET environment variable is not set")
    return os.path.join(file_cabinet_path, uuid_str, "TopDrawer")

def ensure_directory_exists(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Created directory: {path}")
        except OSError as e:
            print(f"Error creating directory: {e}")
            return False
    return True

def download_file(url, destination):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/"
    }
    
    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # First, send a GET request to the URL
        response = session.get(url, headers=headers, stream=True, allow_redirects=True)
        response.raise_for_status()

        # Check if we were redirected to a different URL
        if response.url != url:
            print(f"Redirected to: {response.url}")

        # Get the filename from the Content-Disposition header if available
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = re.findall("filename=(.+)", content_disposition)
            if filename:
                destination = os.path.join(os.path.dirname(destination), filename[0].strip('"'))

        # If no Content-Disposition, use the last part of the URL path
        if not content_disposition:
            parsed_url = urlparse(response.url)
            filename = os.path.basename(parsed_url.path)
            if filename:
                destination = os.path.join(os.path.dirname(destination), filename)

        print(f"Saving file as: {destination}")

        # Now download the file
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

def process_uuid_and_file(id_string, file_path):
    try:
        # Attempt to parse the UUID
        id = uuid.UUID(id_string)
        
        # Get the TopDrawer path for this UUID
        try:
            top_drawer_path = get_top_drawer_path(str(id))
        except EnvironmentError as e:
            print(f"Environment error: {e}")
            return False

        # Check if file_path is a URL
        if file_path.startswith(('http://', 'https://')):
            print(f"Downloading from URL: {file_path}")
            
            # Ensure the directory exists before downloading
            if not ensure_directory_exists(top_drawer_path):
                print("Failed to create directory")
                return False
            
            # Use a placeholder filename, it might be updated in the download_file function
            placeholder_filename = "downloaded_file"
            destination = os.path.join(top_drawer_path, placeholder_filename)
            print(destination)            
            if download_file(file_path, destination):
                print(f"File downloaded successfully: {destination}")
                file_path = destination
            else:
                print("Failed to download file")
                return False
        else:
            print(f"Processing local file: {file_path}")
            # If it's a local file, we might want to copy it to the TopDrawer
            # This step is optional and depends on your requirements
        
        # Here you would add your actual processing logic
        print(f"UUID: {id}")
        print(f"File path: {file_path}")
        
        return True
    except ValueError:
        print("Invalid UUID format")
        return False

# Example usage
try:
    result = process_uuid_and_file("550e8400-e29b-41d4-a716-446655440000", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7402177/pdf/antioxidants-09-00619.pdf")
    print(f"Processing successful: {result}")
except Exception as e:
    print(f"An error occurred: {e}")
