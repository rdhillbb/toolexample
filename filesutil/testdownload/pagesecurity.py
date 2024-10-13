import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random

def download_content(uuid: str, url: str, filename: str) -> str:
    try:
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # Realistic User-Agent and Headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            # Additional headers
            'Referer': 'https://www.thehistorymakers.org/',
            'DNT': '1',  # Do Not Track
            'TE': 'Trailers'
        }

        # First request to get cookies
        base_url = '/'.join(url.split('/')[:3])
        initial_response = session.get(base_url, headers=headers)
        initial_response.raise_for_status()  # Ensure the initial request is successful
        time.sleep(random.uniform(1, 3))  # Random delay

        # Add cookies from the initial request if any
        cookies = initial_response.cookies.get_dict()

        # Request to the actual page with cookies
        response = session.get(url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()

        # Save content
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, "wb") as file:
            file.write(response.content)

        return f"The content from {url} was successfully downloaded and saved as {filename} in the current directory."

    except requests.Timeout:
        return f"Error: The request to {url} timed out after 30 seconds."
    except requests.RequestException as e:
        return f"Error: Failed to download the content. {str(e)}"
    except Exception as e:
        return f"Error: Failed to save the content. {str(e)}"

print(download_content("U", "https://www.thehistorymakers.org/biography/katherine-g-johnson-42", "thehistor.html"))

