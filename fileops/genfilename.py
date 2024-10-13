import sys
sys.path.append("../")
from platforms.deepinfra import call_deepinfra_model

def createfileame(text):
    """
    This function generates a name based on the context of the provided text.
    The name is up to 15 characters long and has no spaces.

    Parameters:
    text (str): The text to use as context for generating the name.

    Returns:
    str: The generated name.
    """

    # Format the prompt string with the provided text
    prompt = f"""
    You are to take the following text and generate a name based on the context of the provided text:

    <context>
    {text}
    </context>

    The name should be up to 15 characters long and have no spaces.
    You are to provide the answer.
    """
    print(prompt)
    # Call the Deep Infra model with the prompt string
    response = call_deepinfra_model("meta-llama/Meta-Llama-3-8B-Instruct", prompt)

    # Extract the generated name from the response
    name = response.strip()

    # Ensure the name is up to 15 characters long and has no spaces
    name = name.replace(" ", "")[:15]

    return name
def genfilenamex(text: str) -> str:
    print("GENFILE", text)
    chat = OpenAI(temperature=0, model="text-davinci-003")
    template = """
 you are to take Text and generate a name based on the context of the provided.  The name should be up to 15 characters. There are to be no spaces.
 You are to provide the Answer.
Text: {query}

Answer: """
    if len(text) > 200:
        text = text[:200]
    prompt_template = PromptTemplate(input_variables=["query"], template=template)
    msg = chat(prompt_template.format(query=text))
    msg = msg.replace("\n", "")
    msg = msg.replace("'", "")
    msg = msg.replace(" ", "")
    return msg


print(
    createfileame(
        "You are to take the following text and generate a name based on the context of the provided text"
    )
 )
