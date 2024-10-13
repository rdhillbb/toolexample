from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

chat = ChatPerplexity(
    temperature=0, pplx_api_key="YOUR_API_KEY", model="pplx-70b-online"
)
chat = ChatPerplexity(temperature=0, model="pplx-70b-online")
system = "You are a helpful assistant."
human = "{input}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat
while True:
    req = input("was me anything to research? ")
    response = chain.invoke({"input": req})
    print(response)
