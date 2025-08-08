# Anthropic Agent

A simple command-line chat application built in Go that provides an interactive interface to chat with Claude (Anthropic's AI assistant).

## Overview

This project demonstrates how to build a basic conversational AI agent using Anthropic's Claude API. The application maintains conversation context and provides a clean terminal-based chat interface.

This project is inspired by Thorsten Ball's tutorial ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent).

## Features

- **Interactive CLI Chat**: Chat with Claude directly from your terminal
- **Conversation Context**: Maintains full conversation history for coherent responses
- **Clean Interface**: Color-coded output to distinguish between user input and Claude's responses
- **Error Handling**: Graceful error handling for API calls and user input
- **Modular Design**: Clean separation between chat logic and API interactions

## Prerequisites

- Go 1.24.3 or later
- Anthropic API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kostola/anthropic-agent.git
cd anthropic-agent
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
You: Hello, how are you today?
Claude: Hello! I'm doing well, thank you for asking. I'm here and ready to help with any questions or tasks you might have. How are you doing today?
You: Can you explain what Go contexts are?
Claude: Go contexts are a powerful feature in Go that provide a way to carry deadlines, cancellation signals, and request-scoped values across API boundaries...
```

## Configuration

The application uses the following default settings:
- **Model**: Claude 3.7 Sonnet Latest
- **Max Tokens**: 1024 per response
- **Input**: Standard input (terminal)

## Dependencies

- [`github.com/anthropics/anthropic-sdk-go`](https://github.com/anthropics/anthropic-sdk-go) - Official Anthropic Go SDK

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## API Reference

This application uses the Anthropic Messages API. For more information about the API capabilities and options, visit the [Anthropic API documentation](https://docs.anthropic.com/).

