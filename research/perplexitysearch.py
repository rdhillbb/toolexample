import requests
import json
import os
import re
from perplexityprompt import topic,systemprompt,SEARCH_PROMPT_PLX

def extract_search_results(response):
    """
    This function extracts search results from a given response.

    Parameters:
    response (dict): A dictionary containing the response from an API call.

    Returns:
    list: A list of dictionaries, where each dictionary contains the keys 'Title', 'URL', and 'Summary'.
          Returns None if no search results are found in the response.
    """
    try:
        # Extract the content of the assistant's message
        content = response['choices'][0]['message']['content']

        # Find the JSON code between the <search_results> tags
        match = re.search(r'<search_results>(.*?)</search_results>', content, re.DOTALL)

        if match:
            # Extract the JSON code
            json_code = match.group(1)

            # Parse the JSON code
            search_results = json.loads(json_code)

            return search_results
        else:
            print("No search results found in the response.")
            return None
    except KeyError as e:
        print(f"Error: {e} not found in the response.")
        return None

class PlexitySearchInput(BaseModel):
    topic: str = Field(description="topic to search, queation or request for internet search")

# Define the tool function with the input schema
@tool("PlexitySearch", args_schema=PlexitySearchInput)
def perplexity_search(topic):
    """
    The perplexity_search function sends a search request to the Perplexity API and extracts the search results.
    It should be called when you want to perform a web search for a specific topic.

    When to Use:
    - Use this function whenever you need to perform a web search for information on a specific topic.

    How to Use:
    - Call the function with the desired search topic as the parameter.

    Parameters:
    - topic (str): The topic to search for.

    Returns:
    - json: A JSON array where each element is in the format:
      - Title: The title of the search result.
      - URL: The URL of the search result.
      - Summary: A summary of the search result.
    - Returns None if the request to the API fails.
    """
    llm_model = os.getenv('PLEX_LLM')
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {os.getenv('API_PERPLEXITY_SDK')}",
        "content-type": "application/json"
    }
    data = {
        "model": llm_model,
        "messages": [
            {
                "role": "system",
                "content": systemprompt
            },
            {
                "role": "user",
                "content": SEARCH_PROMPT_PLX.format(topic=topic)
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception if the request failed
        return extract_search_results(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

print(perplexity_search(topic))

