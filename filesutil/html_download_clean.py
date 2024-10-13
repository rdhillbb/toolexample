import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all text from the page
        text = soup.get_text()

        # Remove extra whitespace and newlines
        clean_text = " ".join(text.split())

        return clean_text
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


# Example usage
url = "https://www.cnn.com"
urls = [
    "https://en.wikipedia.org/wiki/Katherine_Johnson",
    "https://www.britannica.com/biography/Katherine-Johnson-mathematician",
    "https://www.nasa.gov/learning-resources/katherine-johnson-a-lifetime-of-stem/",
    "https://www.nasa.gov/centers-and-facilities/langley/katherine-johnson-biography/",
    "https://www.space.com/katherine-johnson.html",
]

for url in urls:
    extracted_text = scrape_website(url)
    print(extracted_text)
    print("LENGTH",len(extracted_text))
    print("-"*4)
    print()
