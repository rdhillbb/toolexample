import os
import anthropic 
#from anthropic import Anthropic
MAX_TOKENS = 4096
TEMPERATURE = 0
ANTHROPIC_MODEL = "claude-3-opus-20240229"  # Use the appropriate model version
SYSTEM_PROMPT = "You are a helpful expert."

def filename_prompt(TEXT: str) -> str:
    user_prompt = f"""You will be creating a file name based on the following text:
<text>
{TEXT}
</text>
Your task is to create a file name that accurately represents the content of the text. The file name should adhere to the following rules:
1. It must be no longer than 15 characters
2. It cannot contain spaces
3. It cannot contain special characters
4. Numbers are allowed
5. The name should consist of full words or partial words
Before providing your final answer, use the scratchpad to think through your process. Consider the main topic or keywords from the text, and how you can condense them into a concise file name that meets the above criteria.
<scratchpad>
Think through your process here. Consider:
1. What are the main topics or keywords in the text?
2. How can you abbreviate or combine words to fit the 15-character limit?
3. Are there any numbers that would be relevant to include?
4. How can you make the file name descriptive while following the rules?
</scratchpad>
After thinking it through, provide your final file name inside <filename> tags. Remember, the file name should be no longer than 15 characters, contain no spaces or special characters, and can include numbers if relevant. Do not provide your thoughs only provide the filename.
<filename>
"""
    return user_prompt

def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
    return anthropic.Anthropic(api_key=api_key)

def anthropic_llm(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    """
    This function creates a message using the Anthropic API with the given prompts and parameters.
    It returns the content of the response message from the model.
    
    Parameters:
    prompt (str): The user's input or question.
    system_prompt (str): The system prompt to set the context for the AI.
    max_tokens (int): The maximum number of tokens in the response (default: MAX_TOKENS).
    temperature (float): The sampling temperature (default: TEMPERATURE).
    
    Returns:
    str: The content of the response message from the Anthropic API.
    
    Raises:
    Exception: If there's an error in creating the Anthropic message.
    """
    try:
        client = get_anthropic_client()        
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    except Exception as e:
        raise Exception(f"Error creating Anthropic message: {str(e)}")

if __name__ == "__main__":
    text = "Garlic is a polyphenolic and organosulfur enriched nutraceutical spice consumed since ancient times."
    result = anthropic_llm(filename_prompt(text))
    print(result)
