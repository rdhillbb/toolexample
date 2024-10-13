import os
import anthropic
api_key = os.environ.get("ANTHROPIC_API_KEY")
print(dir(anthropic))
anthropic_directory = os.path.dirname(anthropic.__file__)
print(anthropic_directory)
a = anthropic.Anthropic(api_key=api_key)

