"""
Read file tool implementation.
Provides file reading functionality with schema caching.
"""

from typing import Any, Dict
from agent import ToolDefinition


class ReadFileTool(ToolDefinition):
    """
    Tool for reading file contents.
    Provides file reading functionality with cached schema for performance.
    """

    def __init__(self):
        # Cache the schema at initialization to avoid recomputation
        self._input_schema = {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The relative path of a file in the working directory."
                }
            },
            "required": ["path"]
        }

    def name(self) -> str:
        """Return the tool name."""
        return "read_file"

    def description(self) -> str:
        """Return the tool description."""
        return "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names."

    def input_schema(self) -> Dict[str, Any]:
        """Return the cached JSON schema for tool input validation."""
        return self._input_schema

    def execute(self, path: str) -> str:
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