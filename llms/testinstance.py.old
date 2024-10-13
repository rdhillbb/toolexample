from llmobjects import LLMObject

# Test instances
llm_openai = LLMObject("ChatOpenAI:gpt-4", streaming=True)
response_openai = llm_openai.send_message("Provide the health benefits of Garlic")
print("ChatOpenAI:", response_openai)
print()
llm_anthropic = LLMObject("ChatAnthropic:claude-1.3")
response_anthropic = llm_anthropic.send_message("Hello, how are you?")
print("ChatAnthropic:", response_anthropic)
print()
# llm_cohere = LLMObject("ChatCohere:command-xlarge-nightly")
# response_cohere = llm_cohere.send_message("Hello, how are you?")
# print("ChatCohere:", response_cohere)

print()
llm_deepinfra = LLMObject("ChatDeepInfra:meta-llama/Meta-Llama-3-70B-Instruct")
response_deepinfra = llm_deepinfra.send_message("Hello, how are you?")
print("ChatDeepInfra:", response_deepinfra)

print()
# llm_google = LLMObject("ChatGoogleGenerativeAI:gemini-pro")
# response_google = llm_google.send_message("Hello, how are you?")
# print("ChatGoogleGenerativeAI:", response_google)

print()
llm_ollama = LLMObject("ChatOllama:llama2", stream=False)
response_ollama = llm_ollama.send_message("Hello, how are you?")
print("ChatOllama:", response_ollama)

print()
llm_groq = LLMObject("ChatGroq:mixtral-8x7b-32768")
response_groq = llm_groq.send_message("Hello, how are you?")
print("ChatGroq:", response_groq)
