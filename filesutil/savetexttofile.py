import os
import pathlib
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from filesutil.genfilename import genfilename
decription = "used to save text in a specified file"
name = "save_text_infile"


class SaveTextToFileInput(BaseModel):
    # Input for saving text in a specified file
    uuid: str = Field(...,description="UUID")
    text: str = Field(..., description="Text to be saved")
    filename: str = Field(
        ..., description="to be used to save text in a named text file."
    )


class SaveTextToFileTool(BaseTool):
    name = "save_text_infile"
    description = "used to save text in a specified file"

    def _run(self,uuid:str, text: str, filename: str):
        save_text_response = savetextinfile(uuid,text, filename)

        return save_text_response

    def _arun(self, text: str, filename: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = SaveTextToFileInput


def savetextinfile(uuid,text, filename):
    try:
        # Get the file cabinet path from the environment variable
        file_cabinet_path = os.environ.get("GOVBOTIC_INGESTION_STORAGE")

        # Check if the file cabinet path exists
        if not file_cabinet_path:
            return "Error File Not Saved: File cabinet path not found in environment variable"

        # Create the top drawer path
        top_drawer_path = os.path.join(file_cabinet_path,uuid, "Top Drawer")

        # Create the top drawer directory if it does not exist
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)

        # Create the file path
        file_path = os.path.join(top_drawer_path, filename)

        # Write the text to the file
        with open(file_path, "w") as file:
            file.write(text)

        return f"The file {filename} was saved successfully at: {top_drawer_path}"

    except IOError as e:
        return f"Error File Not Saved : Failed to save file '{filename}': {e}"


def writetext(uuid:str, txt: str) -> str:
    try:
        # Get the file cabinet path from the environment variable
        file_cabinet_path = os.environ.get("GEPPETTO_FILE_CABINET")

        # Check if the file cabinet path exists
        if not file_cabinet_path:
            return "Error File Not Saved: File cabinet path not found in environment variable"

        # Create the top drawer path
        top_drawer_path = os.path.join(file_cabinet_path,uuid, "Top Drawer")
        # Generate file name
        filename = genfilename(txt) + ".txt"
        # Create the top drawer directory if it does not exist
        pathlib.Path(top_drawer_path).mkdir(parents=True, exist_ok=True)

        # Create the file path
        file_path = os.path.join(top_drawer_path, filename)

        # Write the text to the file
        with open(file_path, "w") as file:
            file.write(txt)

        return f"The file {filename} was saved successfully at Top Drawer."

    except IOError as e:
        return f"Error File Not Saved : Failed to save file '{filename}': {e}"


class SaveTextInput(BaseModel):
    # Input for saving text
    txt: str = Field(..., description="Text to be saved")


class SaveTextTool(BaseTool):
    name = "savetext"
    # description = "used to save a filename isn't specified, the text will be saved to a file with a name derived from the text's content."
    description = "saves text when no filename is provided.The filename will be based on content of the text."

    def _run(self, txt: str):
        rsp = writetext(txt)
        return rsp

    def _arun(self, txt: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = SaveTextInput
