# Go Agent Implementation

A command-line AI agent built in Go that provides an interactive interface to chat with Claude (Anthropic's AI assistant) with tool-calling capabilities.

## Overview

This Go implementation demonstrates how to build a functional AI agent using Anthropic's Claude API with tool integration. The agent can maintain conversation context, execute tools, and provide a clean terminal-based interface for interaction.

This implementation is inspired by Thorsten Ball's tutorial ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent).

## Features

- **Interactive CLI Chat**: Chat with Claude directly from your terminal
- **Tool Integration**: Extensible tool system allowing Claude to execute functions
- **File Operations**: Built-in `read_file` tool for examining file contents
- **Conversation Context**: Maintains full conversation history for coherent responses
- **Clean Interface**: Color-coded output to distinguish between user input, Claude's responses, and tool executions
- **Error Handling**: Graceful error handling for API calls, tool execution, and user input
- **Modular Design**: Clean separation between chat logic, API interactions, and tool definitions
- **Type-Safe Tools**: JSON schema generation for tool input validation

## Prerequisites

- Go 1.24.3 or later
- Anthropic API key

## Installation

1. Navigate to the Go implementation directory:
```bash
cd golang
```

2. Install dependencies:
```bash
go mod tidy
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

Run the application:
```bash
go run main.go
```

The application will start an interactive chat session. Type your messages and press Enter to send them to Claude. Use `Ctrl+C` to quit the application.

### Example Session
```
Chat with Claude (use 'ctrl-c' to quit)
You: Hello, can you read the main.go file and tell me what it does?
Claude: I'll read the main.go file to understand what it does.

tool: read_file({"path":"main.go"})

Based on the main.go file, this is a Go application that implements an AI agent with tool-calling capabilities...

You: What tools are available?
Claude: Based on the code I just read, there is currently one tool available:

1. **read_file** - This tool allows me to read the contents of files in the working directory...
```

## Configuration

The application uses the following default settings:
- **Model**: Claude 3.7 Sonnet Latest
- **Max Tokens**: 1024 per response
- **Input**: Standard input (terminal)
- **Tools**: `read_file` tool enabled by default

## Architecture

The agent follows a simple but powerful architecture:

1. **Agent Loop**: Continuously processes user input and Claude responses
2. **Tool System**: Extensible framework for adding new capabilities
3. **Schema Generation**: Automatic JSON schema creation for type-safe tool inputs
4. **Tool Execution**: Safe execution of tools with error handling and result formatting

### Adding New Tools

To add a new tool, create a struct in the `tools/` package that implements the `agent.ToolDefinition` interface:

```go
// In tools/my_tool.go
type MyTool struct {
    inputSchema anthropic.ToolInputSchemaParam
}

type MyToolInput struct {
    Param string `json:"param" jsonschema_description:"Description of the parameter"`
}

func NewMyTool() *MyTool {
    return &MyTool{
        inputSchema: GenerateSchema[MyToolInput](),
    }
}

func (t *MyTool) Name() string { return "my_tool" }
func (t *MyTool) Description() string { return "What the tool does" }
func (t *MyTool) InputSchema() anthropic.ToolInputSchemaParam { return t.inputSchema }
func (t *MyTool) Execute(input json.RawMessage) (string, error) {
    // Tool implementation
}
```

Then register it in `main.go`:
```go
agentTools := []agent.ToolDefinition{
    tools.NewReadFileTool(),
    tools.NewListFilesTool(),
    tools.NewMyTool(), // Add your new tool here
}
```

### Code Organization

The codebase is organized into focused packages:

#### **`main.go`**
- Application entry point
- Tool registration and agent initialization
- User input handling

#### **`agent/` Package**
- **`agent.go`**: Core agent implementation with conversation loop
- **`ToolDefinition` interface**: Contract that all tools must implement
- Agent configuration and Claude API integration

#### **`tools/` Package**
- **`tools.go`**: Shared utilities like `GenerateSchema[T]()` function
- **`read_file.go`**: File reading tool implementation
- **`list_files.go`**: Directory listing tool implementation
- Each tool in its own file for modularity

## Dependencies

- [`github.com/anthropics/anthropic-sdk-go`](https://github.com/anthropics/anthropic-sdk-go) - Official Anthropic Go SDK
- [`github.com/invopop/jsonschema`](https://github.com/invopop/jsonschema) - JSON Schema generation library

## Go-Specific Features

- **Package Architecture**: Clean separation of concerns with dedicated packages
- **Interface-Driven Design**: Tools implement a common interface for extensibility
- **Schema Caching**: Input schemas are computed once and cached for performance
- **Type Safety**: Leverages Go's strong typing system for tool input validation
- **JSON Schema Generation**: Automatic schema creation from Go structs
- **Memory Efficiency**: Compiled binary with minimal runtime overhead
- **Concurrent Safe**: Built with Go's concurrency patterns in mind
- **Cross-Platform**: Single binary deployment across different operating systems

## Building for Distribution

To build a standalone binary:
```bash
go build -o agent
./agent
```

To build for different platforms:
```bash
# Linux
GOOS=linux GOARCH=amd64 go build -o agent-linux

# Windows
GOOS=windows GOARCH=amd64 go build -o agent-windows.exe

# macOS
GOOS=darwin GOARCH=amd64 go build -o agent-macos
```