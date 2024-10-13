import requests
from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field


class GoogleSearchInput(BaseModel):
    query: str = Field(..., description="Request will be a NLP question or request")


@tool("GoogleSearch", args_schema=GoogleSearchInput)
def internet_search_google(query: str) -> list:
    """
    Perform an internet search using Google's Custom Search API for the given query.
    
    This function uses Google's Custom Search JSON API to perform an internet search.
    It requires a valid API key and Custom Search Engine ID to function properly.
    
    :param query: The search term to look up on the internet
    :return: A list of search results or an error message
    """
    # Google Custom Search JSON API endpoint
    api_url = "https://www.googleapis.com/customsearch/v1"
    
    # You need to obtain these from Google Cloud Console and Custom Search Engine
    api_key = "AIzaSyDMc-nSaaNrmdf543z4PaGnKifVHBf7RII"
    search_engine_id = "948201cf72a504311"
    
    # Check if API key and search engine ID are specified
    if api_key == "YOUR_GOOGLE_API_KEY" or search_engine_id == "YOUR_SEARCH_ENGINE_ID":
        return ["API key or Search Engine ID not specified for internet search"]
    
    params = {
        "q": query,
        "key": api_key,
        "cx": search_engine_id
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Parse the JSON response
        results = response.json()
        
        # Process and return the results
        return results.get("items", [])
    
    except requests.RequestException as e:
        if "401" in str(e):
            return ["API key rejected for internet search"]
        else:
            return [f"An error occurred during internet search: {str(e)}"]

# Example usage
#results = internet_search_google.invoke("Looking for information on Katherin Johnson")
#if isinstance(results[0], str) and results[0].startswith(("API key", "An error")):
#    print(f"Error: {results[0]}")
#else:
#  for result in results:
#      print(result["title"], result["link"])
