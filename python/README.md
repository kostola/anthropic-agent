# Python Agent Implementation

A command-line AI agent built in Python using LangChain that provides an interactive interface to chat with Claude (Anthropic's AI assistant) with tool-calling capabilities.

## Overview

This Python implementation demonstrates how to build a functional AI agent using LangChain and Anthropic's Claude API. The agent leverages LangChain's powerful tool integration system and provides the same functionality as the Go implementation with Python's flexibility and ecosystem.

## Features

- **Interactive CLI Chat**: Chat with Claude directly from your terminal
- **LangChain Integration**: Leverages LangChain's tool system for seamless integration
- **Tool Calling Support**: Built-in `read_file` tool with extensible architecture
- **Conversation History**: Maintains full conversation context using LangChain messages
- **Color-coded Output**: Clean interface distinguishing user input, Claude responses, and tool executions
- **Error Handling**: Robust error handling for API calls, tool execution, and user input
- **Modular Design**: Clean separation between agent logic, tools, and main execution
- **Pydantic Validation**: Type-safe tool inputs using Pydantic models

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
- Use `Ctrl+C` to quit

### Example Session
```
Chat with Claude (use 'ctrl-c' to quit)
You: Hello, can you read the main.py file and tell me what it does?
Claude: I'll read the main.py file to understand what it does.

tool: read_file({"path": "main.py"})

Based on the main.py file, this is a Python application that implements an AI agent using LangChain...

You: What tools are available?
Claude: Based on the code I just read, there is currently one tool available:

1. **read_file** - This tool allows me to read the contents of files in the working directory...
```

## Configuration

The application uses the following default settings:
- **Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **Max Tokens**: 1024 per response
- **Temperature**: 0 (deterministic responses)
- **Input**: Standard input (terminal)
- **Tools**: `read_file` tool enabled by default

## Architecture

The Python implementation consists of three main modules:

### `main.py`
- Entry point that mirrors the Go main function
- Initializes the ChatAnthropic client
- Sets up the conversation loop
- Handles user input and graceful shutdown

### `agent.py`
- `Agent` class that manages the conversation flow
- Handles message history and tool execution
- Integrates with LangChain's tool binding system
- Provides error handling and user interaction

### `tools.py`
- `ReadFileTool` implementation using LangChain's `BaseTool`
- Pydantic models for input validation
- Extensible architecture for adding new tools

## Adding New Tools

To add a new tool, create a class that inherits from `BaseTool`:

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    param: str = Field(description="Description of the parameter")

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "Description of what the tool does"
    args_schema: Type[BaseModel] = MyToolInput
    
    def _run(self, param: str) -> str:
        # Tool implementation
        return "Tool result"

# Add to tools list in main.py
tools = [read_file_tool, MyTool()]
```

## Dependencies

- **langchain-anthropic**: LangChain integration for Anthropic Claude
- **langchain-core**: Core LangChain functionality for messages and tools
- **pydantic**: Data validation and settings management using Python type annotations
- **anthropic**: Official Anthropic Python SDK

## Python-Specific Features

- **Dynamic Typing**: Leverages Python's flexibility while maintaining type safety with Pydantic
- **LangChain Ecosystem**: Access to extensive LangChain tool library and integrations
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
from tools import read_file_tool
print('Tool test:', read_file_tool.invoke({'path': 'main.py'})[:100] + '...')
"
```

## Comparison with Go Implementation

**Similarities:**
- Same conversation loop logic
- Same tool execution pattern
- Same error handling approach
- Same user interface with colored output
- Same Claude model capabilities

**Python Advantages:**
- LangChain's extensive tool ecosystem
- More flexible for rapid prototyping
- Rich Python ecosystem for data processing
- Dynamic configuration and runtime modifications

**Go Advantages:**
- Type safety at compile time
- Single binary deployment
- Better performance for production workloads
- Memory efficiency 