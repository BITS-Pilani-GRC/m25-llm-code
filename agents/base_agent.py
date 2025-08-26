"""
Base Coding Agent - Simple foundation for LLM-powered coding agents
"""

import json
from typing import Dict, List, Any

class Tool:
    """Simple tool wrapper for agent capabilities"""
    def __init__(self, name: str, description: str, function):
        self.name = name
        self.description = description
        self.function = function
    
    def execute(self, **kwargs):
        """Execute the tool with given parameters"""
        try:
            return {"success": True, "result": self.function(**kwargs)}
        except Exception as e:
            return {"success": False, "error": str(e)}

class BaseCodingAgent:
    """
    Simple base class for coding agents
    Students can extend this for different capabilities
    """
    
    def __init__(self, llm_client, tools: List[Tool] = None):
        self.llm = llm_client
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.conversation_history = []
    
    def add_tool(self, tool: Tool):
        """Add a new tool to the agent"""
        self.tools[tool.name] = tool
    
    def get_tool_descriptions(self) -> str:
        """Get formatted descriptions of available tools for LLM"""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool and return the result"""
        if tool_name not in self.tools:
            return {"success": False, "error": f"Tool '{tool_name}' not found"}
        
        print(f"🔧 Executing tool: {tool_name} with {kwargs}")
        result = self.tools[tool_name].execute(**kwargs)
        print(f"📋 Tool result: {result}")
        return result
    
    def think(self, prompt: str) -> str:
        """
        Use LLM to reason about the problem
        This is where the intelligence happens
        """
        system_prompt = f"""You are a helpful coding agent. You have access to these tools:

{self.get_tool_descriptions()}

Analyze the given problem and respond clearly. If you need to use tools, mention which ones and why.
Be concise and educational - this is for students learning about coding agents.
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            # {"role": "user", "content": prompt}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        response = self.llm.complete(messages)
        
        # Store in history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response

    def solve(self, problem: str) -> str:
        """
        Main entry point - solve a coding problem
        Override this in specific agent versions
        """
        return self.think(problem)
