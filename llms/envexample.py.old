import os
from llmobjects import LLMObject
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Note: This should be done in a script
variable_name = "LLMMODEL"
variable_value = "ChatAnthropic:claude-1.3"
os.environ[variable_name] = variable_value

# Python code
llm = os.getenv(variable_name)
print("Platform:", llm)

# Define a prompt
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
output_parser = StrOutputParser()

# Initialize LLMObject with the environment variable
llm_instance = LLMObject(llm, temperature=1, max_tokens=4096).llm_instance
chain2 = prompt | llm_instance | output_parser

print(chain2.invoke({"topic": "ice cream"}))
