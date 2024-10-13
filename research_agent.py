from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from rich.console import Console
from config import readconfig
from llms.llmobjects import LLMObject
from dotenv import load_dotenv
from researchprompt import  getsysmpmt
class ResearchAgentExecutor:
    def __init__(self):
        load_dotenv()
        self.llm = LLMObject(
            "ChatOpenAI:gpt-4o", temperature=.4, streaming=False, max_tokens=4096
            #"ChatOpenAI:gpt-4o-mini", temperature=.4, streaming=False, max_tokens=4096
        ).llm_instance
        self.system_prompt = self._load_system_prompt()
        self.agent_executor = self._setup_agent_executor()

    def _load_system_prompt(self):
        return getsysmpmt()

    def _setup_agent_executor(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        fileTools = readconfig("researchconfig.yaml")
        llm_with_tools = self.llm.bind_tools(fileTools)
        #llm_with_tools = dict(fileTools)
        print(type(llm_with_tools))

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        return AgentExecutor(
            agent=agent,
            tools=fileTools,
            verbose=True,
            max_iterations=15,
            handle_parsing_errors=False,
        )

    def execute(self, input_query):
        return self.agent_executor.invoke({"input": input_query})

# Example usage (can be commented out or removed when using as a module)
if __name__ == "__main__":
    agent = ResearchAgentExecutor()
    
    while True:
        query = input("Enter your query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        response = agent.execute(query)
        print(response["output"])
