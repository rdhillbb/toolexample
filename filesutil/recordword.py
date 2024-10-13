from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type


class RecordWordInput(BaseModel):
    # Input for recording a word

    wrd: str = Field(..., description="Word to be recorded")


class RecordWordTool(BaseTool):
    name = "recordword"
    description = "Record the word provided to the student Human. This function is to be called prior to giving the student the word. There is one input."

    def _run(self, wrd: str):
        enterword(wrd)
        print(wrd)
        return "word recorded"

    def _arun(self, wrd: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = RecordWordInput


def enterword(wd: str) -> str:
    return "entered"
