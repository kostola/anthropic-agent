# Anthropic Agent

A command-line AI agent that provides an interactive interface to chat with Claude (Anthropic's AI assistant) with tool-calling capabilities. This repository contains two implementations: **Go** and **Python**.

## Overview

This project demonstrates how to build functional AI agents using Anthropic's Claude API with tool integration. Both implementations can maintain conversation context, execute tools, and provide a clean terminal-based interface for interaction.

The project is inspired by Thorsten Ball's tutorial ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent) and showcases the same agent logic implemented in two different programming languages with their respective ecosystems.

## Features

Both implementations provide:
- **Interactive CLI Chat**: Chat with Claude directly from your terminal
- **Tool Integration**: Extensible tool system allowing Claude to execute functions
- **File Operations**: Built-in `read_file` tool for examining file contents
- **Conversation Context**: Maintains full conversation history for coherent responses
- **Clean Interface**: Color-coded output to distinguish between user input, Claude's responses, and tool executions
- **Error Handling**: Graceful error handling for API calls, tool execution, and user input
- **Modular Design**: Clean separation between chat logic, API interactions, and tool definitions

## Implementations

### 🐹 Go Implementation
Located in the [`golang/`](./golang/) directory.
- **Type-Safe Tools**: JSON schema generation for tool input validation
- **Performance**: Compiled binary with minimal runtime overhead
- **Deployment**: Single binary for easy distribution

[📖 Go Implementation Details →](./golang/README.md)

### 🐍 Python Implementation  
Located in the [`python/`](./python/) directory.
- **LangChain Integration**: Leverages LangChain's extensive tool ecosystem
- **Pydantic Validation**: Type-safe tool inputs using Pydantic models
- **Flexibility**: Easy to extend and prototype new features

[📖 Python Implementation Details →](./python/README.md)

## Quick Start

### Prerequisites
- Anthropic API key
- Go 1.24.3+ (for Go implementation) OR Python 3.8+ (for Python implementation)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/kostola/anthropic-agent.git
cd anthropic-agent
```

2. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. Choose your implementation:

**Go:**
```bash
cd golang
go mod tidy
go run main.go
```

**Python:**
```bash
cd python
pip install -r requirements.txt
python main.py
```

### Example Session
Both implementations provide the same interactive experience:
```
Chat with Claude (use 'ctrl-c' to quit)
You: Hello, can you read the README.md file and tell me what this project does?
Claude: I'll read the README.md file to understand what this project does.

tool: read_file({"path":"README.md"})

Based on the README.md file, this is a project that implements AI agents using Anthropic's Claude API...

You: What tools are available?
Claude: Based on the code, there are currently two tools available:

1. **read_file** - This tool allows me to read the contents of files in the working directory
2. **list_files** - This tool allows me to list files and directories at a given path...
```

## Configuration

Both implementations use similar default settings:
- **Model**: Claude 3.5 Sonnet Latest
- **Max Tokens**: 1024 per response  
- **Input**: Standard input (terminal)
- **Tools**: `read_file` and `list_files` tools enabled by default

## Architecture

Both implementations follow a similar architecture pattern:

1. **Agent Loop**: Continuously processes user input and Claude responses
2. **Tool System**: Extensible framework for adding new capabilities  
3. **Input Validation**: Type-safe tool inputs (JSON schema in Go, Pydantic in Python)
4. **Tool Execution**: Safe execution of tools with error handling and result formatting

The core logic remains consistent across both implementations, with language-specific optimizations and patterns.

## Project Structure

```
anthropic-agent/
├── golang/                  # Go implementation
│   ├── main.go             #   - Application entry point
│   ├── agent/              #   - Agent package
│   │   └── agent.go        #     - Core agent logic and interfaces
│   ├── tools/              #   - Tools package
│   │   ├── tools.go        #     - Shared utilities
│   │   ├── read_file.go    #     - File reading tool
│   │   └── list_files.go   #     - Directory listing tool
│   ├── go.mod              #   - Go dependencies
│   ├── go.sum              #   - Dependency checksums
│   └── README.md           #   - Go-specific documentation
├── python/                  # Python implementation  
│   ├── main.py             #   - Entry point
│   ├── agent.py            #   - Agent class and conversation logic
│   ├── tools.py            #   - Tool implementations
│   ├── requirements.txt    #   - Python dependencies
│   └── README.md           #   - Python-specific documentation
├── LICENSE                  # MIT License
└── README.md               # This file (general overview)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Both implementations welcome contributions! See the specific README files for implementation-specific development guidelines.

## License

This project is open source and available under the [MIT License](LICENSE).

## API Reference

Both implementations use the Anthropic Messages API. For more information about the API capabilities and options, visit the [Anthropic API documentation](https://docs.anthropic.com/).

