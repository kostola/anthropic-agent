"""
Agent implementation using LangChain and Anthropic Claude.
Mirrors the functionality of the Go agent implementation.
"""

import json
from typing import Any, Callable, Dict, List, Optional, Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class Agent:
    """
    Agent class that handles conversation with Claude using LangChain.
    Equivalent to the Go Agent struct.
    """
    
    def __init__(
        self,
        client: ChatAnthropic,
        get_user_message: Callable[[], Tuple[str, bool]],
        tools: List[BaseTool]
    ):
        self.client = client
        self.get_user_message = get_user_message
        self.tools = tools
        self.tools_by_name = {tool.name: tool for tool in tools}
    
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
        Equivalent to runInference in Go.
        """
        # Bind tools to the client
        client_with_tools = self.client.bind_tools(self.tools)
        
        # Invoke the model
        response = client_with_tools.invoke(conversation)
        return response
    
    def _execute_tool(self, tool_call) -> ToolMessage:
        """
        Execute a tool call and return the result.
        Equivalent to executeTool in Go.
        """
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool_call_id = tool_call["id"]
        
        if tool_name not in self.tools_by_name:
            print(f"\u001b[92mtool\u001b[0m: {tool_name}({json.dumps(tool_input)})")
            return ToolMessage(
                content="tool not found",
                tool_call_id=tool_call_id
            )
        
        tool = self.tools_by_name[tool_name]
        
        print(f"\u001b[92mtool\u001b[0m: {tool_name}({json.dumps(tool_input)})")
        
        try:
            result = tool.invoke(tool_input)
            return ToolMessage(
                content=str(result),
                tool_call_id=tool_call_id
            )
        except Exception as e:
            return ToolMessage(
                content=str(e),
                tool_call_id=tool_call_id
            ) 