import brotli
import logging
import os
import pathlib
import re
import sys
from typing import Annotated, List, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool

sys.path.append("../")
from filesutil.genfilename import create_filename
from filesutil.checkgarble import is_garbled
from filesutil.clean_html import scrape_website, write_to_file, url_to_filename, get_current_datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_file_type(filename: str) -> bool:
    """Check if the file is either a .txt or .md file."""
    return filename.lower().endswith(('.txt', '.md'))

class AppendFileToAFileInput(BaseModel):
    uuid: str = Field(description="UUID")
    source_file: str = Field(description="Source File")
    target_file: str = Field(description="Target/Destination file")

@tool("AppendFileToAFile", args_schema=AppendFileToAFileInput)
def append_file_content(uuid: str, source_file: str, target_file: str) -> str:
    """
    File Operation
    Appends the content of the source file to the target file.
    Both source and target files must be either .txt or .md files.
    If the target file does not exist, it will be created.

    Args:
    uuid (str): Unique identifier for the user or session
    source_file (str): Path to the source file.
    target_file (str): Path to the target file.

    Returns:
    str: A message indicating success or describing an error.
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        src_file = os.path.join(top_drawer_path, source_file)
        trg_file = os.path.join(top_drawer_path, target_file)

        # Check file extensions
        if not is_valid_file_type(source_file) or not is_valid_file_type(target_file):
            return "Error: Only .txt and .md files are allowed for appending."

        # Read content from source file
        with open(src_file, 'r', encoding='utf-8') as sf:
            content = sf.read()

        # Append content to target file (create if it does not exist)
        with open(trg_file, 'a', encoding='utf-8') as tf:
            tf.write('\n' + content)

        return f"Content from {source_file} was successfully appended to {target_file}."
    except FileNotFoundError as fnf_error:
        return f"Error: {fnf_error.filename} does not exist."
    except Exception as e:
        return f"Error: {str(e)}"

class DownloadContentInput(BaseModel):
    uuid: str = Field(description="UUID")
    url: str = Field(description="URL of the content to download")
    filename: str = Field(description="Name of the file to save the downloaded content")

@tool("DownloadContent", args_schema=DownloadContentInput)
def download_content(uuid: str, url: str, filename: str) -> str:
    """
    Used for File Operation Only
    Downloads content from the given URL and saves it to a file in the top drawer.
    Handles various content types including webpages, PDFs, CSVs, images, and other file types.
    The request is made to appear as if it's coming from a browser and times out after 30 seconds.

    Args:
    uuid (str): Unique identifier for the user or session
    url (str): URL of the content to download
    filename (str): Name of the file to save the downloaded content

    Returns:
    str: A message indicating success or describing an error
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)

        file_path = os.path.join(top_drawer_path, filename)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }

        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
        mode = 'wb' if 'text' not in content_type and 'json' not in content_type else 'w'
        encoding = 'utf-8' if 'text' in content_type or 'json' in content_type else None

        with open(file_path, mode, encoding=encoding) as file:
            if mode == 'wb':
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            else:
                file.write(response.text)

        return f"The content from {url} was successfully downloaded and saved as {filename} in the top drawer."
    except requests.Timeout:
        return f"Error: The request to {url} timed out after 30 seconds."
    except requests.RequestException as e:
        return f"Error: Failed to download the content. {str(e)}"
    except Exception as e:
        return f"Error: Failed to save the content. {str(e)}"

class CleanHTMLInput(BaseModel):
    uuid: str = Field(description="UUID")
    html_filename: str = Field(description="html file to be cleaned")
    output_filename: str = Field(description="Name of the file to save the cleaned content")

@tool("CleanHTMLContent", args_schema=CleanHTMLInput)
def clean_html_content(uuid: str, html_filename: str, output_filename: str) -> str:
    """
    File Operation
    Cleans an HTML file and saves the cleaned text to a new file in the top drawer.
    Use this function when:
    - You have an HTML file that needs to be cleaned
    - You want to extract readable text from HTML
    - You need to remove HTML tags and script content from a webpage

    Args:
    uuid (str): Unique identifier for the user or session
    html_filename (str): Name of the HTML file to be cleaned
    output_filename (str): Name of the file to save the cleaned content

    Returns:
    str: A message indicating success or describing an error
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(top_drawer_path, output_filename)

        # Read the HTML file
        htm_filename = os.path.join(top_drawer_path, html_filename)
        with open(htm_filename, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove all style and script tags
        for tag in soup(['style', 'script']):
            tag.decompose()

        # Extract the cleaned text
        cleaned_text = ' '.join(soup.stripped_strings)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(cleaned_text)

        return f"The HTML content was successfully cleaned and saved as {output_filename} in the top drawer."
    except Exception as e:
        return f"Error: Failed to clean HTML content and save the file. {str(e)}"

class WebpageDownloadInput(BaseModel):
    uuid: str = Field(description="UUID")
    url: str = Field(description="URL of the webpage to download")

@tool("DownloadWebpage", args_schema=WebpageDownloadInput)
def download_webpage(uuid: str, url: str) -> str:
    """
    Used for File Operation 
    Downloads a webpage from the given URL and saves it to a file in the top drawer.
    The request is made to appear as if it's coming from a browser and times out after 10 seconds.
    Handles various compression methods and encoding issues.

    Use this function when:
    - You need to save the content of a webpage for offline access or analysis
    - You want to create a local copy of a webpage
    - You need to mimic a browser request to avoid restrictions
    - You want to ensure the request doesn't hang indefinitely

    Args:
    uuid (str): Unique identifier for the user or session
    url (str): URL of the webpage to download

    Returns:
    str: A message indicating success or describing an error
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File cabinet path not found in environment variable"
        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)

        filename = url_to_filename(url)
        filename = get_current_datetime() + "_" + filename 
        file_path = os.path.join(top_drawer_path, filename)

        content = scrape_website(url)
        write_to_file(file_path, url, content)

        return f"Webpage content from {url} was saved to {file_path}"
    except requests.Timeout:
        return f"Error: The request to {url} timed out after 10 seconds."
    except requests.RequestException as e:
        return f"Error: Failed to download the webpage. {str(e)}"
    except Exception as e:
        return f"Error: Failed to save the webpage content. {str(e)}"

class SaveTextInput(BaseModel):
    uuid: str = Field(description="UUID")
    txt: str = Field(description="Text to be saved")

class GetFilePathInput(BaseModel):
    uuid: str = Field(description="UUID")
    filename: str = Field(description="Name of the file")

@tool("GetFilePath", args_schema=GetFilePathInput)
def get_file_path(uuid: str, filename: str) -> str:
    """
    Used for File Operation
    Returns the file path of a given file located in the top directory.

    Use this function when:
    - You need to get the full path of a specific file
    - You want to perform operations that require the file's absolute path

    Args:
    uuid (str): Unique identifier for the user or session
    filename (str): Name of the file

    Returns:
    str: The full path of the file, or an error message if the operation fails
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        file_path = os.path.join(top_drawer_path, filename)

        if not os.path.exists(file_path):
            return f"Error: File '{filename}' not found in the top drawer for this UUID."

        return file_path
    except Exception as e:
        return f"Error: Failed to get file path. {str(e)}"

class ReadFileInput(BaseModel):
    uuid: str = Field(description="UUID")
    filename: str = Field(description="Name of the file")

@tool("ReadFileContents", args_schema=ReadFileInput)
def read_file_contents(uuid: str, filename: str) -> str:
    """
    File Operation
    Reads the contents of a file and returns the entire text.

    Use this function when:
    - You need to retrieve the full content of a specific file
    - You want to process or analyze the contents of a file

    Args:
    uuid (str): Unique identifier for the user or session
    filename (str): Name of the file to be read

    Returns:
    str: The entire contents of the file as a string, or an error message if the operation fails
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        file_path = os.path.join(top_drawer_path, filename)

        if not os.path.exists(file_path):
            return f"Error: File '{filename}' not found in the top drawer for this UUID."

        with open(file_path, "r") as file:
            contents = file.read()

        return contents
    except Exception as e:
        return f"Error: Failed to read file contents. {str(e)}"

@tool("SaveTextToCreatedFile", args_schema=SaveTextInput)
def writetext(uuid: str, txt: str) -> str:
    """
    File Operation
    Save text to a file in the top drawer when no file name is specified.

    Args:
    uuid (str): Unique identifier for the user or session
    txt (str): Text to be saved to the file

    Returns:
    str: A message indicating success or describing an error
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File Not Saved. File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        fn = create_filename(txt)
        print(fn)
        filename = f"{fn}.txt"
        print(filename) 
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(top_drawer_path, filename)
        print(file_path) 
        with open(file_path, "w") as file:
            file.write(txt)

        return f"The file {filename} was saved successfully in Top Drawer."
    except IOError as e:
        print("$$$ RRROR",e)
        return f"Error: File Not Saved. Failed to save file '{filename}': {str(e)}"

class FileOperationInput(BaseModel):
    uuid: str = Field(description="UUID")
    txt: str = Field(description="Text to be saved or appended")
    filename: str = Field(description="Name of the file")

class ListFilesInput(BaseModel):
    uuid: str = Field(description="UUID")

@tool("CreateAndWriteFile", args_schema=FileOperationInput)
def create_and_write_file(uuid: str, txt: str, filename: str) -> str:
    """
    File Operation
    Creates a new file with the given filename and writes the text to it.
    If the file already exists, it will be overwritten.

    Use this function when:
    - You want to create a new file with specific content
    - You want to overwrite an existing file with new content
    - You're not concerned about preserving any existing content in the file

    Args:
    uuid (str): Unique identifier for the user or session
    txt (str): Text to be written to the file
    filename (str): Name of the file to be created or overwritten

    Returns:
    str: A message indicating success or describing an error
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File Not Saved. File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)

        file_path = os.path.join(top_drawer_path, filename)

        with open(file_path, "w") as file:
            file.write(txt)

        return f"The file {filename} was created and saved successfully in Top Drawer."
    except Exception as e:
        return f"Error: Failed to create and write to file. {str(e)}"

@tool("AppendOrCreateFile", args_schema=FileOperationInput)
def append_or_create_file(uuid: str, txt: str, filename: str) -> str:
    """
    File Operation
    Appends text to an existing file or creates a new file if it doesn't exist.

    Use this function when:
    - You want to add content to an existing file without overwriting its current content
    - You want to create a new file if it doesn't exist yet
    - You're not sure if the file exists and want to safely add content in either case

    Args:
    uuid (str): Unique identifier for the user or session
    txt (str): Text to be appended to the existing file or written to a new file
    filename (str): Name of the file to be appended to or created

    Returns:
    str: A message indicating success or describing an error
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return "Error: File Not Saved. File cabinet path not found in environment variable"

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)

        file_path = os.path.join(top_drawer_path, filename)

        # Open the file in append mode, which creates the file if it doesn't exist
        with open(file_path, "a") as file:
            file.write(txt)

        action = "appended to" if os.path.getsize(file_path) > len(txt) else "created and written to"
        return f"The text was successfully {action} the file {filename} in Top Drawer."
    except Exception as e:
        return f"Error: Failed to append to or create file. {str(e)}"

@tool("ListTopDrawerFiles", args_schema=ListFilesInput)
def list_top_drawer_files(uuid: str) -> List[str]:
    """
    File Operation
    Lists all files in the top drawer for the given UUID.

    Use this function when:
    - You need to see all files stored in a user's top drawer
    - You want to check if a specific file exists in the top drawer
    - You need to perform operations on multiple files in the top drawer

    Args:
    uuid (str): Unique identifier for the user or session

    Returns:
    List[str]: A list of filenames in the top drawer, or an error message if the operation fails
    """
    try:
        file_cabinet_path = os.environ.get("GOVBOTIC_FILE_CABINET")
        if not file_cabinet_path:
            return ["Error: File cabinet path not found in environment variable"]

        top_drawer_path = os.path.join(file_cabinet_path, uuid, "TopDrawer")

        if not os.path.exists(top_drawer_path):
            return ["No files found. The top drawer does not exist for this UUID."]

        files = [f for f in os.listdir(top_drawer_path) if os.path.isfile(os.path.join(top_drawer_path, f))]

        if not files:
            return ["The top drawer is empty."]

        return files
    except Exception as e:
        return [f"Error: Failed to list files in top drawer. {str(e)}"]
#print(writetext("UUID-001-0001-110","Stay until the break of down. Take a walk in the park so many things there"))
