"""
Version 1: Code Reader Agent
Purpose: Demonstrate how LLM can read and understand code

Key Learning Points:
- LLM can analyze code structure and purpose
- Simple tool integration (read_file)
- One-shot analysis pattern
"""

import os
from base_agent import BaseCodingAgent, Tool

def read_file_tool(file_path: str) -> str:
    """Tool to read a file and return its contents"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    return f"Content of {file_path}:\n{content}"

class CodeReaderAgent(BaseCodingAgent):
    """
    Version 1: Agent that can read and analyze code
    
    Capabilities:
    - Read source code files
    - Explain what code does
    - Predict outputs for given inputs
    - Identify code patterns and structure
    """
    
    def __init__(self, llm_client):
        # Initialize with read-only tools
        tools = [
            Tool("read_file", "Read the contents of a file", read_file_tool)
        ]
        super().__init__(llm_client, tools)
    
    def analyze_code(self, file_path: str, question: str = None) -> str:
        """
        Analyze code in a file and answer questions about it
        
        Args:
            file_path: Path to the code file
            question: Optional specific question about the code
            
        Returns:
            Analysis of the code
        """
        print(f"🔍 CodeReader analyzing: {file_path}")
        
        # Step 1: Read the file
        file_result = self.execute_tool("read_file", file_path=file_path)
        
        if not file_result["success"]:
            return f"❌ Error reading file: {file_result['error']}"
        
        file_content = file_result["result"]
        
        # Step 2: Analyze with LLM
        if question:
            prompt = f"""Please analyze this code and answer the specific question:

{file_content}

Question: {question}

Provide a clear, educational explanation that helps students understand the code."""
        else:
            prompt = f"""Please analyze this code and explain:

{file_content}

Explain in simple terms:
1. What does this code do?
2. What are the main components/functions?
3. How does it work step by step?
4. Any notable patterns or techniques used?

Keep the explanation clear and educational for students."""

        analysis = self.think(prompt)
        return analysis
    
    def predict_output(self, file_path: str, input_example: str) -> str:
        """
        Predict what the code would output for a given input
        
        Args:
            file_path: Path to the code file
            input_example: Example input to trace through
            
        Returns:
            Predicted output explanation
        """
        print(f"🎯 CodeReader predicting output for: {file_path}")
        
        # Read the file
        file_result = self.execute_tool("read_file", file_path=file_path)
        
        if not file_result["success"]:
            return f"❌ Error reading file: {file_result['error']}"
        
        file_content = file_result["result"]
        
        # Predict output with LLM
        prompt = f"""Given this code:

{file_content}

If we run this code with the input: {input_example}

Please trace through the execution step by step and predict:
1. What would be the output?
2. Show the step-by-step execution
3. Explain the reasoning

Be precise and educational."""

        prediction = self.think(prompt)
        return prediction


# Simple testing functions (no framework needed)
def test_code_reader():
    """Simple test function to demonstrate CodeReader capabilities"""
    print("🧪 Testing CodeReader Agent...")
    
    # This would normally use a real LLM client
    # For demo, we'll create a mock
    class MockLLM:
        def complete(self, messages):
            return "This is a simple function that calculates the area of a circle using the formula π * r²."
    
    agent = CodeReaderAgent(MockLLM())
    
    # Test with mock - in real use, you'd have actual files
    print("✅ CodeReader agent created successfully")
    print("Available tools:", list(agent.tools.keys()))

if __name__ == "__main__":
    test_code_reader()
