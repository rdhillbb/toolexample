import sys
from langchain_core.output_parsers import StrOutputParser
from typing import List, Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from promptconfig import getprompts
sys.path.append("../")
from llms.llmobjects import LLMObject
def evaluate(question: str, context: str) -> str:
    """
    Evaluate and proofread text based on a given question.

    This function uses a language model to assess how well the provided text
    answers the given question. It suggests improvements for relevance,
    accuracy, completeness, clarity, and structure.

    Args:
        question (str): The question that the text should address.
        context (str): The text to be evaluated and proofread.

    Returns:
        str: A string containing suggested improvements for the text.
    """
    eprompt = getprompts().evaluator_prompt
    prompt = ChatPromptTemplate.from_template(eprompt)
    model = LLMObject("ChatAnthropic:claude-3-opus-20240229", temperature=0, max_tokens=4096).llm_instance
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    
    print("EVALUATING")
    rsp = chain.invoke({"question": question, "text": context})
    
    return f"Evaluation and proofreading complete. Improvement suggestions:\n{rsp}"

def xevaluate(question: str, context: str) -> str:
    eprompt = getprompts().evaluator_prompt
    prompt = ChatPromptTemplate.from_template(eprompt)

    model  = LLMObject("ChatAnthropic:claude-3-opus-20240229", temperature=1, max_tokens=4096).llm_instance
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    #rsp = chain.invoke({"input": question, "context": context})
    rsp = chain.invoke({"text": context})
    print(" EVALUATING")

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=4096,
        timeout=None,
        max_retries=3,
    )
    model = LLMObject("ChatOpenAI:gpt-4o", temperature=1, max_tokens=4096).llm_instance
    eprompt = getprompts().stage2_eval_prompt
    prompt = ChatPromptTemplate.from_template(eprompt)
    print(rsp)
    chain = prompt | model | output_parser
    rsp = chain.invoke({"input": rsp, "text": context})

    return "Finacl Draft Evaluation complete. "+ rsp


Eeval_description = (
    "This API evaluates the provided text based on the given question or request. "
    "If no improvements are necessary, it will return 'Text is okay'. "
    "Otherwise, it will return the enhanced text."
)

eval_description = (
"Evaluate and proofread text based on a given question."
"A string containing suggested improvements for the text."
)

class EvaluateInput(BaseModel):
    """Input for Evaluate tool."""

    query: str = Field(..., description="Question/Request")
    text: str = Field(..., description="Text to be evaluated based on question/request")


class EvaluateTool(BaseTool):
    name = "evaluator_tool"
#    description = (
#        "This tool evaluates the provided text based on the given question or request."
#    )
    description = eval_description
    def _run(self, query: str, text: str):
        resp = evaluate(query, text)
        return resp

    def _arun(self, query: str, text: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = EvaluateInput


class XEvaluateInput(BaseTool):
    # Used for General information query string for Wikipedia"

    query: str = Field(..., description="Question/Request")
    text: str = Field(..., description="Text to be evaluated based on question/request")


class XEvaluateTool(BaseTool):
    name = "evaluator tool"
    description: str = eval_description

    def _run(self, query: str, text: str):
        resp = evaluate(query, text)

        return resp

    def _arun(self, info: str):
        raise

    args_schema: Optional[Type[BaseModel]] = EvaluateInput
