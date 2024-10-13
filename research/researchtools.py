import sys
from langchain.tools import BaseTool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from research.evaluater import EvaluateTool
sys.path.append("../")

wikipedia_description = (
    "The Wikipedia search API is essential for foundational knowledge across subjects, offering "
    "comprehensive overviews, historical context, and research groundwork. It is perfect for initial "
    "research, fact verification, and identifying further research queries. Ideal for obtaining "
    "general information and precise, reliable data, it seamlessly complements TavilySearchResults for deeper, "
    "current insights. For best results, use specific names or Wikidata QIDs."
)


tavily_description = (
    "Tavily is a search API optimized for AI, delivering accurate and trusted "
    "information from internet sources swiftly. It collects and organizes data "
    "from diverse fields, including finance, coding, and news. Ideal for use "
    "when answering questions, conducting comprehensive research, and staying updated "
    "on current events, Tavily simplifies complex search tasks into a single API call, "
    "supporting efficient decision-making and detailed inquiries."
)


def getgeneralinfo(info: str) -> str:
    wikipedia = WikipediaAPIWrapper()
    resp = wikipedia.run(info)
    return resp


class GetGeneralInfoInput(BaseModel):
    # Used for General information query string for Wikipedia"

    query: str = Field(
        ..., description="Search Tool:Instruction/queation or query for Wikipedia"
    )


class GetGeneralInfoTool(BaseTool):
    name = "getgeneralinfo"
    description: str = wikipedia_description

    def _run(self, query: str):
        resp = getgeneralinfo(query)

        return resp

    def _arun(self, info: str):
        raise


###
def getresearchtools():
    tav = TavilySearchResults(max_results=8)
    print(tav.description)
    tav.description = tavily_description
    return [EvaluateTool(),GetGeneralInfoTool(), tav, DuckDuckGoSearchRun()]


###
