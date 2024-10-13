import os
import pathlib
import requests
import brotli
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_webpage(uuid: str, url: str, filename: str) -> str:
    """
    Downloads a webpage from the given URL and saves it to a file in the current directory.
    Handles Brotli compression and sets appropriate headers for the NASA website.
    """
    try:
        file_path = os.path.join(os.getcwd(), filename)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        logger.info(f"Sending request to: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")

        content_type = response.headers.get('Content-Type', '').lower()
        logger.info(f"Content-Type: {content_type}")
        
        encoding = response.encoding
        logger.info(f"Detected encoding: {encoding}")

        content_encoding = response.headers.get('Content-Encoding', '').lower()
        logger.info(f"Content-Encoding: {content_encoding}")

        if 'br' in content_encoding:
            logger.info("Attempting to decompress Brotli content")
            try:
                content = brotli.decompress(response.content)
                logger.info("Brotli decompression successful")
            except brotli.error as e:
                logger.error(f"Brotli decompression failed: {str(e)}")
                logger.info("Falling back to raw content")
                content = response.content
        elif 'gzip' in content_encoding:
            content = response.content  # requests automatically decompresses gzip
        else:
            content = response.content

        if 'text' in content_type or 'html' in content_type:
            encoding = encoding if encoding else 'utf-8'
            try:
                decoded_content = content.decode(encoding)
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode with {encoding}, falling back to utf-8")
                decoded_content = content.decode('utf-8', errors='replace')
            
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(decoded_content)
            logger.info(f"Content saved as text using UTF-8 encoding")
            return f"Webpage downloaded and saved as text to {filename}"
        else:
            with open(file_path, "wb") as file:
                file.write(content)
            logger.info("Content saved as binary")
            return f"Webpage downloaded and saved as binary to {filename}"

    except requests.RequestException as e:
        logger.error(f"Error downloading webpage: {str(e)}")
        return f"Error downloading webpage: {str(e)}"
    except IOError as e:
        logger.error(f"Error saving webpage: {str(e)}")
        return f"Error saving webpage: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"

def main():
    #url = "https://www.nasa.gov/centers-and-facilities/langley/katherine-johnson-biography/"
    url = "https://www.britannica.com/biography/Katherine-Johnson-mathematician"
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path) or "index.html"
    filename = f"{filename}.html" if not filename.endswith('.html') else filename

    print("NASA Webpage Downloader")
    print(f"Attempting to download: {url}")
    print(f"Saving as: {filename}")

    result = download_webpage("test_user", url, filename)
    print("\nResult:", result)

    if os.path.exists(filename):
        print(f"\nFile saved successfully. File size: {os.path.getsize(filename)} bytes")
        print(f"You can find the downloaded file at: {os.path.abspath(filename)}")
        
        # Print the first few lines of the file for verification
        print("\nFirst few lines of the downloaded file:")
        with open(filename, 'r', encoding='utf-8') as file:
            print(file.read(500))
    else:
        print("\nFile was not saved successfully.")

if __name__ == "__main__":
    main()
