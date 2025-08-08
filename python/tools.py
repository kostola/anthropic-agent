"""
Tool implementations for the agent.
Contains the read_file tool equivalent to the Go implementation.
"""

import os
from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    """Input schema for the read_file tool."""
    path: str = Field(
        description="The relative path of a file in the working directory."
    )


class ReadFileTool(BaseTool):
    """
    Read file tool that reads the contents of a given relative file path.
    Equivalent to the ReadFile function in Go.
    """
    
    name: str = "read_file"
    description: str = (
        "Read the contents of a given relative file path. "
        "Use this when you want to see what's inside a file. "
        "Do not use this with directory names."
    )
    args_schema: Type[BaseModel] = ReadFileInput
    
    def _run(self, path: str) -> str:
        """
        Execute the read file operation.
        
        Args:
            path: The relative path of the file to read
            
        Returns:
            The contents of the file as a string
            
        Raises:
            Exception: If the file cannot be read
        """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            raise Exception(f"Error reading file {path}: {str(e)}")


# Create an instance of the tool
read_file_tool = ReadFileTool() 