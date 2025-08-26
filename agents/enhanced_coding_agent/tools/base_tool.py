"""
Base Tool Class for Enhanced Coding Agent

All tools inherit from this base class to ensure consistent interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import json

class BaseTool(ABC):
    """
    Base class for all agent tools
    
    Each tool must implement:
    - execute(): Main functionality
    - get_description(): Tool description for LLM
    - get_schema(): Parameter schema for LLM function calling
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters
        
        Returns:
            Dict with 'success', 'result', and optional 'error' keys
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get human-readable description of what this tool does
        Used by LLM to understand when to use this tool
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for tool parameters
        Used for LLM function calling
        """
        pass
    
    def format_result(self, success: bool, result: Any = None, error: str = None) -> Dict[str, Any]:
        """Helper to format tool results consistently"""
        response = {"success": success}
        if result is not None:
            response["result"] = result
        if error is not None:
            response["error"] = error
        return response
    
    def __str__(self):
        return f"{self.name}: {self.get_description()}"
