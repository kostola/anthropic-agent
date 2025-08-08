"""
List files tool implementation.
Provides directory listing functionality with schema caching.
"""

import json
import os
from typing import Any, Dict, Optional
from agent import ToolDefinition


class ListFilesTool(ToolDefinition):
    """
    Tool for listing files and directories.
    Provides directory listing functionality with cached schema for performance.
    """

    def __init__(self):
        # Cache the schema at initialization to avoid recomputation
        self._input_schema = {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Optional relative path to list files from. Defaults to current directory if not provided."
                }
            },
            "required": []
        }

    def name(self) -> str:
        """Return the tool name."""
        return "list_files"

    def description(self) -> str:
        """Return the tool description."""
        return "List files and directories at a given path. If no path is provided, lists files in the current directory."

    def input_schema(self) -> Dict[str, Any]:
        """Return the cached JSON schema for tool input validation."""
        return self._input_schema

    def execute(self, path: Optional[str] = None) -> str:
        """
        Execute the list files operation.

        Args:
            path: Optional relative path to list files from. Defaults to current directory.

        Returns:
            JSON string containing the list of files and directories

        Raises:
            Exception: If the directory cannot be listed
        """
        try:
            target_dir = path if path else "."

            files = []
            for root, dirs, filenames in os.walk(target_dir):
                # Get relative path from target directory
                rel_root = os.path.relpath(root, target_dir)

                # Add directories
                for dir_name in dirs:
                    if rel_root == ".":
                        files.append(f"{dir_name}/")
                    else:
                        files.append(f"{rel_root}/{dir_name}/")

                # Add files
                for filename in filenames:
                    if rel_root == ".":
                        files.append(filename)
                    else:
                        files.append(f"{rel_root}/{filename}")

            # Sort for consistent output
            files.sort()

            return json.dumps(files)

        except Exception as e:
            raise Exception(f"Error listing files in {path or '.'}: {str(e)}")