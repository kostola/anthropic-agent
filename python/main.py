"""
Main script for the Python agent implementation.
Mirrors the functionality of main.go using LangChain and Anthropic Claude.
"""

import sys
from typing import Tuple
from langchain_anthropic import ChatAnthropic
from agent import Agent
from tools import read_file_tool


def get_user_message() -> Tuple[str, bool]:
    """
    Get user input from stdin.
    
    Returns:
        Tuple of (message, success) where success indicates if input was read
    """
    try:
        line = input()
        return line, True
    except EOFError:
        return "", False


def main():
    """
    Main function that initializes the agent and starts the conversation loop.
    """
    # Initialize the Anthropic client using LangChain
    client = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",  # Latest Claude 3.5 Sonnet
        max_tokens=1024,
        temperature=0
    )
    
    # Define available tools
    tools = [read_file_tool]
    
    # Create and run the agent
    agent = Agent(client, get_user_message, tools)
    error = agent.run()
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main() 