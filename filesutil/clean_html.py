import requests
from datetime import datetime
from bs4 import BeautifulSoup
import random
import re
from urllib.parse import urlparse

def get_current_datetime():
    """
    Returns the current date and time in the format yyyymmdd_HHMMSS.
    
    :return: A string representing the current date and time.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")
def get_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    return random.choice(user_agents)

def scrape_website(url):
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        clean_text = " ".join(text.split())
        return clean_text
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

def write_to_file(file, url, content):
    """
    Writes the scraped content to a file, creating it if it doesn't exist or overwriting if it does.
    
    :param filename: The name of the file to write to
    :param url: The URL of the scraped website
    :param content: The scraped and cleaned content
    """
    with open(file, 'w', encoding='utf-8') as file:
        file.write(f"URL: {url}\n")
        file.write(f"Content length: {len(content)}\n")
        file.write("Content:\n")
        file.write(content)
        file.write("\n\n" + "-"*50 + "\n\n")

def url_to_filename(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract the domain and path
    domain = parsed_url.netloc
    path = parsed_url.path
    
    # Remove 'www.' if present
    domain = re.sub(r'^www\.', '', domain)
    
    # Replace dots and slashes with underscores
    domain = domain.replace('.', '_')
    path = path.replace('/', '_')
    
    # Remove any special characters
    domain = re.sub(r'[^\w\-_]', '', domain)
    path = re.sub(r'[^\w\-_]', '', path)
    
    # Combine domain and path
    filename = f"{domain}{path}"
    
    # Trim if the filename is too long (optional, adjust max_length as needed)
    max_length = 200
    if len(filename) > max_length:
        filename = filename[:max_length]
    
    # Add file extension
    filename += ".txt"
    
    return filename

def main():
    urls = [
        "https://en.wikipedia.org/wiki/Katherine_Johnson",
        "https://www.britannica.com/biography/Katherine-Johnson-mathematician",
        "https://www.nasa.gov/learning-resources/katherine-johnson-a-lifetime-of-stem/",
        "https://www.nasa.gov/centers-and-facilities/langley/katherine-johnson-biography/",
        "https://www.space.com/katherine-johnson.html",
    ]

    # This is just an example. In a real scenario, you would open the file
    # outside of this function and pass it as an argument.
    with open("scraped_content.txt", "w", encoding="utf-8") as file:
        for url in urls:
            content = scrape_website(url)
            write_to_file(file, url, content)

if __name__ == "__main__":
    main()
