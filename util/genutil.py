import re

def get_tag_text(text):
    pattern = r'<filename>(.*?)</filename>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def creatflnprompt(TEXT: str) -> str:
    user_prompt = f"""You will be creating a file name based on the following text:
<text>
{TEXT}
</text>
Your task is to create a file name that accurately represents the content of the text. The file name should adhere to the following rules:
1. It must be no longer than 25 characters
2. It cannot contain spaces
3. It cannot contain special characters
4. Numbers are not allowed
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
