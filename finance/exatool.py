from exa_py import Exa
from typing import List, Optional, Type
from langchain_community.tools import format_tool_to_openai_function
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

def improverequest(text: str) -> str:
    print("GENFILE", text)
    chat = OpenAI(temperature=0)
    template = """
Rewrite the given Text to create a question or request that will elicit more detailed and insightful responses.
You are to provide the Answer.
Text: {query}

Answer: """
    prompt_template = PromptTemplate(input_variables=["query"], template=template)

    try:
        msg = chat.invoke(prompt_template.format(query=text))
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    return msg

def exagetnews(query:str)->str:
    exa = Exa("1255d1da-de47-4b91-aba7-9acc991819c2")
    #newquery = improverequest(query)
    #newquery = query
    response = exa.search_and_contents(
               query,
               num_results=10,
               use_autoprompt=True,
               text={"max_characters": 2500, "include_html_tags": True},
              )
    return response
class ExaGetNewsInput(BaseModel):
    """Input for to receive yahoo news on stock"""

    query: str = Field(..., description="concise questions or requests about companies, market conditions, stocks, or financial reports.")


class ExaGetNewsTool(BaseTool):
    name = "exagetnews"
    #description = "Only use for Market news and insights on stocks and indices, offering comprehensive articles and in-depth analysis, delivering extensive coverage with a global perspective to support informed decision-making.for financial and market usage only"
    description = "This function delivers general market news, company financial statuses, and global market insights. It offers comprehensive articles and in-depth analysis with extensive global coverage, designed exclusively for financial and market contexts. This tool supports informed decision-making by providing crucial, up-to-date information tailored for investors and analysts."
    def _run(self, query: str):
        news = exagetnews(query) 

        return news

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = ExaGetNewsInput 
#print(exagetnews("I would like information on Googles financials for 2023"))
