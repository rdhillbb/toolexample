import os
import glob
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type


def listfilesindir(uuid:str,directory: str) -> str:
    """
    This function lists all files documents in the middle drawer specified by the environment variable 'GEPPETTO_FILE_CABINET'
    with the extension 'middleDrawer'.
    Improvement has been made to handle exceptions and errors more efficiently.
    """
    try:
        # Getting the directory from the environment variable 'GEPPETTO_FILE_CABINET'
        storage = os.getenv("GOVBOTIC_INGESTION_STORAGE")
        # If directory path is None
        if storage is None:
            raise ValueError(
                "The environment variable 'GOVBOTIC_INGESTION_STORAGE' is not set."
            )

        # Create directory if it doesn't exist
#        if not os.path.exists(directory):
#            print(f"The directory {directory} does not exist. Creating it now.")
#            os.makedirs(directory)

        # Constructing the final file path with the specified extension '.middleDrawer'
        file_path = os.path.join(storage,uuid,directory+"/*")

        # Listing all files in the directory with the specified extension
        files = glob.glob(file_path)
        # If no files with specified extension are found in the directory
        print(files)
        if not files:
            print("No files found in the File Drawer")

        # Printing all found files
        listoffiles = ""
        for file in files:
            listoffiles += f"File: {file}\n"
        return listoffiles
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function
#from langchain.tools import BaseTool
#from pydantic import BaseModel, Field
#from typing import Optional, Type


class ListFilesInDirInput(BaseModel):
    # Input for list files in directory
    uuid: str = Field(...,description="UUID")
    directory: str = Field(..., description="Directory to list files from")


class ListFilesInDirTool(BaseTool):
    name = "listfilesindir"
    # description = "Use the command to list files in the designated File Drawer. Specify the File Drawer,i.e Top Drawer, Middle Drawer, Bottom Drawer."
    description = "Use the command to list files in the designated file drawer. Accept any case-insensitive variant of the keywords 'Top', 'Middle', or 'Bottom', including combinations with 'drawer' (e.g., 'top drawer', 'MIDDLE', 'Bottom Drawer'). Standardize all such inputs to 'Top Drawer', 'Middle Drawer', or 'Bottom Drawer' respectively."

    def _run(self, uuid:str,directory: str):
        file_list = listfilesindir(uuid,directory)

        return file_list

    def _arun(self, directory: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = ListFilesInDirInput


"""
# Improvements made:
# - Removed unnecessary try-except block and else block
# - Implemented proper error handling using FileNotFoundError
# - Used f-strings for better readability
# - Removed unnecessary print statement
# - Added type hints to the function signature
"""

"""
description = This is a utility that extracts the path information of a specific file or document for ingestion purposes located in the top file drawer. To use it, you must supply the name of the file or document you wish to ingest.
name = getfileIntopdrawer
"""


def getfileIntopdrawer(uuid:str,file_name: str) -> str:
    file_path = os.path.join(
        os.environ.get("GOVBOTIC_INGESTION_STORAGE"),uuid, "Top Drawer", file_name
    )

    if os.path.exists(file_path):
        return file_path
    else:
        return f"Error: The file '{file_name}' could not be found"


# Test the function
class GetFileInTopDrawerInput(BaseModel):
    # Input for getting file in top drawer
    uuid: str = Field(...,description="UUID")
    file_name: str = Field(
        ..., description="Name of the file or document you wish to ingest"
    )


class GetFileInTopDrawerTool(BaseTool):
    name = "getfileIntopdrawer"
    description = "This is a utility that extracts the path information of a specific file or document for ingestion purposes located in the top file drawer. To use it, you must supply the name of the file or document you wish to ingest."
    description = "This utility extracts the path information from a file or document located in the top file drawer for ingestion purposes. To use this utility, please provide both the UUID and the file or document you want to ingest."


    def _run(self, uuid:str, file_name: str):
        file_path = getfileIntopdrawer(uuid,file_name)

        return file_path

    def _arun(self, file_name: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetFileInTopDrawerInput


"""
description = Use this  utility that extracts the path information of a specific file or document located in the topDrawer for ingestion purposes. To use it, you must supply the name of the file or document you wish to process.
name= listtopdrawerfiles
"""


class ListTopDrawerFilesInput(BaseModel):
    uuid: str = Field(...,description="UUID")
    dir: str = Field(
        ..., description="Name of the file or document you wish to process"
    )


class ListTopDrawerFilesTool(BaseTool):
    name = "listtopdrawerfiles"
    description = "Use this utility list files and  documents located in the topDrawer. To use it, you must supply the name ."

    def _run(self, uuid:str,dir: str) -> str:
        file_list = listtopdrawerfiles(uuid,dir)

        return file_list

    def _arun(self, dir: str) -> str:
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = ListTopDrawerFilesInput


def listtopdrawerfiles(uuid:str,dir: str) -> str:
    file_list = []

    # Check if directory exists
    # if Not os.path.isdir(dir):

    if True:
        # Get the full path of the topDrawer directory
        directory = os.getenv("GOVBOTIC_INGESTION_STORAGE")
        #top_drawer_path = os.path.join(directory,uuid, "Top Drawer")
        top_drawer_path = os.path.join(directory,uuid, dir)
        list(dir)
        print(top_drawer_path)
        # Check if the topDrawer directory exists
        if os.path.isdir(top_drawer_path):
            # Iterate through all files in the topDrawer directory
            for file_name in os.listdir(top_drawer_path):
                # Get the full path of the file
                file_path = os.path.join(top_drawer_path, file_name)

                # Check if the file is a regular file
                if os.path.isfile(file_path):
                    file_list.append(file_name)
        else:
            raise ValueError("topDrawer directory does not exist.")

    # Return the list of files in topDrawer :as a string
    return ", ".join(file_list)
