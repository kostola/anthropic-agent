# Python Agent Implementation

A command-line AI agent built in Python using LangChain that provides an interactive interface to chat with Claude (Anthropic's AI assistant) with tool-calling capabilities.

## Overview

This Python implementation demonstrates how to build a functional AI agent using LangChain and Anthropic's Claude API. The agent leverages LangChain's powerful tool integration system and provides flexible, extensible tool-calling capabilities with Python's rich ecosystem.

## Features

- **Interactive CLI Chat**: Chat with Claude directly from your terminal
- **LangChain Integration**: Leverages LangChain's tool system for seamless integration
- **Tool Calling Support**: Built-in `read_file` tool with extensible architecture
- **Conversation History**: Maintains full conversation context using LangChain messages
- **Color-coded Output**: Clean interface distinguishing user input, Claude responses, and tool executions
- **Error Handling**: Robust error handling for API calls, tool execution, and user input
- **Modular Design**: Clean separation between agent logic, tools, and main execution
- **Type Safety**: Interface-driven design with comprehensive type hints

## Prerequisites

- Python 3.8 or later
- Anthropic API key

## Installation

1. Navigate to the Python implementation directory:
```bash
cd python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

Run the agent:
```bash
python main.py
```

The agent will start an interactive chat session. You can:
- Type messages to chat with Claude
- Claude can use the `read_file` tool to read files in your current directory
- Claude can use the `list_files` tool to list files and directories
- Use `Ctrl+C` to quit

### Example Session
```
Chat with Claude (use 'ctrl-c' to quit)
You: Hello, can you read the main.py file and tell me what it does?
Claude: I'll read the main.py file to understand what it does.

tool: read_file({"path": "main.py"})

Based on the main.py file, this is a Python application that implements an AI agent using LangChain...

You: What tools are available?
Claude: Based on the code I just read, there are currently two tools available:

1. **read_file** - This tool allows me to read the contents of files in the working directory
2. **list_files** - This tool allows me to list files and directories at a given path...
```

## Configuration

The application uses the following default settings:
- **Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **Max Tokens**: 1024 per response
- **Temperature**: 0 (deterministic responses)
- **Input**: Standard input (terminal)
- **Tools**: `read_file` and `list_files` tools enabled by default

## Architecture

The Python implementation is organized into focused packages:

### `main.py`
- Application entry point
- Tool registration and agent initialization
- User input handling and graceful shutdown

### `agent/` Package
- **`agent.py`**: Core agent implementation with conversation loop
- **`ToolDefinition` interface**: Abstract base class that all tools must implement
- Agent configuration and Claude API integration

### `tools/` Package
- **`read_file.py`**: File reading tool implementation
- **`list_files.py`**: Directory listing tool implementation
- Each tool implements the `ToolDefinition` interface
- Schema caching for optimal performance

## Adding New Tools

To add a new tool, create a class in the `tools/` package that implements the `ToolDefinition` interface:

```python
# In tools/my_tool.py
from typing import Any, Dict
from agent import ToolDefinition

class MyTool(ToolDefinition):
    def __init__(self):
        # Cache the schema at initialization
        self._input_schema = {
            "type": "object",
            "properties": {
                "param": {
                    "type": "string",
                    "description": "Description of the parameter"
                }
            },
            "required": ["param"]
        }

    def name(self) -> str:
        return "my_tool"

    def description(self) -> str:
        return "Description of what the tool does"

    def input_schema(self) -> Dict[str, Any]:
        return self._input_schema

    def execute(self, param: str) -> str:
        # Tool implementation
        return "Tool result"
```

Then register it in `main.py`:
```python
from tools import ReadFileTool, ListFilesTool, MyTool

agent_tools = [
    ReadFileTool(),
    ListFilesTool(),
    MyTool(),  # Add your new tool here
]
```

## Dependencies

- **langchain-anthropic**: LangChain integration for Anthropic Claude
- **langchain-core**: Core LangChain functionality for messages and tools
- **anthropic**: Official Anthropic Python SDK

## Python-Specific Features

- **Package Architecture**: Clean separation of concerns with dedicated packages
- **Interface-Driven Design**: Tools implement a common abstract base class for extensibility
- **Schema Caching**: Input schemas are computed once and cached for performance
- **Dynamic Typing**: Leverages Python's flexibility while maintaining type safety
- **LangChain Integration**: Seamless integration with LangChain's tool ecosystem
- **Rapid Prototyping**: Easy to modify and extend with new functionality
- **Rich Error Messages**: Detailed error information for debugging
- **Package Management**: Standard pip/requirements.txt dependency management

## Development

### Running in Development Mode

For development, you can install the package in editable mode:

```bash
pip install -e .
```

### Virtual Environment Setup

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Testing

To test the implementation:

```bash
python -c "
from tools import ReadFileTool
tool = ReadFileTool()
print('Tool test:', tool.execute(path='main.py')[:100] + '...')
"
```