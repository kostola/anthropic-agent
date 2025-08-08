"""
Agent implementation using LangChain and Anthropic Claude.
Provides interface-based design for extensible tool integration.
"""

import json
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage


class ToolDefinition(ABC):
    """
    Interface that all tools must implement.
    Defines the contract for agent tool implementations.
    """

    @abstractmethod
    def name(self) -> str:
        """Return the tool name."""
        pass

    @abstractmethod
    def description(self) -> str:
        """Return the tool description."""
        pass

    @abstractmethod
    def input_schema(self) -> dict:
        """Return the tool input schema."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with the given input."""
        pass


class Agent:
    """
    Agent class that handles conversation with Claude using LangChain.
    Manages conversation flow and tool execution with interface-based design.
    """

    def __init__(
        self,
        client: ChatAnthropic,
        get_user_message: Callable[[], Tuple[str, bool]],
        tools: List[ToolDefinition]
    ):
        self.client = client
        self.get_user_message = get_user_message
        self.tools = tools
        self.tools_by_name = {tool.name(): tool for tool in tools}

    def run(self) -> Optional[str]:
        """
        Main conversation loop.
        Returns error message if any, None on success.
        """
        conversation: List[BaseMessage] = []

        print("Chat with Claude (use 'ctrl-c' to quit)")

        read_user_input = True
        try:
            while True:
                if read_user_input:
                    print("\u001b[94mYou\u001b[0m: ", end="", flush=True)
                    user_input, ok = self.get_user_message()
                    if not ok:
                        break

                    conversation.append(HumanMessage(content=user_input))

                # Run inference
                try:
                    response = self._run_inference(conversation)
                    conversation.append(response)
                except Exception as e:
                    return f"Inference error: {str(e)}"

                # Process response and handle tools
                tool_messages = []
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    for tool_call in response.tool_calls:
                        result = self._execute_tool(tool_call)
                        tool_messages.append(result)
                else:
                    # Display text response
                    print(f"\u001b[93mClaude\u001b[0m: {response.content}")

                if len(tool_messages) == 0:
                    read_user_input = True
                    continue

                read_user_input = False
                conversation.extend(tool_messages)

        except KeyboardInterrupt:
            print("\nGoodbye!")
        except Exception as e:
            return str(e)

        return None

    def _run_inference(self, conversation: List[BaseMessage]) -> AIMessage:
        """
        Run inference with the conversation history.
        Sends conversation to Claude and returns the response.
        """
        # Convert tools to Anthropic native format
        anthropic_tools = []
        for tool in self.tools:
            anthropic_tools.append({
                "name": tool.name(),
                "description": tool.description(),
                "input_schema": tool.input_schema()
            })

        # Bind tools to the client
        client_with_tools = self.client.bind(tools=anthropic_tools)

        # Invoke the model
        response = client_with_tools.invoke(conversation)
        return response

    def _execute_tool(self, tool_call) -> ToolMessage:
        """
        Execute a tool call and return the result.
        Handles tool execution and error management.
        """
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool_call_id = tool_call["id"]

        if tool_name not in self.tools_by_name:
            print(f"\u001b[92mTool\u001b[0m: {tool_name}({json.dumps(tool_input)})")
            return ToolMessage(
                content="tool not found",
                tool_call_id=tool_call_id
            )

        tool = self.tools_by_name[tool_name]

        print(f"\u001b[92mTool\u001b[0m: {tool_name}({json.dumps(tool_input)})")

        try:
            result = tool.execute(**tool_input)
            return ToolMessage(
                content=str(result),
                tool_call_id=tool_call_id
            )
        except Exception as e:
            return ToolMessage(
                content=str(e),
                tool_call_id=tool_call_id
            )