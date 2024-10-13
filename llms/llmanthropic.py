import os
import anthropic
import sys
sys.path.append("../")
from util.genutil import creatflnprompt, get_tag_text

MAX_TOKENS = 4096
TEMPERATURE = 0
SYSTEM_PROMPT = "You are a helpful expert."

def anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
    return anthropic.Anthropic(api_key=api_key)

def anthropic_llm(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    try:
        model = os.environ.get('ANTHROPIC_MODEL', 'claude-3-opus-20240229')
        client = anthropic_client()
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        raise Exception(f"Error creating Anthropic message: {str(e)}")

if __name__ == "__main__":
    prompt = creatflnprompt("This is the story of a man named Brady that had 6 kids.")
    result = anthropic_llm(prompt)
    print(get_tag_text(result))

