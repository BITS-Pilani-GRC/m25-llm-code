"""
Version 2: Code Fixer Agent
Purpose: Demonstrate how LLM can fix bugs in code

Key Learning Points:
- LLM can identify and fix bugs
- Read → Fix → Verify cycle
- Simple execution and verification
- Iterative problem solving
"""

import os
import subprocess
import tempfile
from base_agent import BaseCodingAgent, Tool

def read_file_tool(file_path: str) -> str:
    """Tool to read a file and return its contents"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    return f"Content of {file_path}:\n{content}"

def write_file_tool(file_path: str, content: str) -> str:
    """Tool to write content to a file"""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        raise Exception(f"Failed to write file: {str(e)}")

def execute_python_tool(file_path: str) -> str:
    """Tool to execute a Python file and return the output"""
    try:
        result = subprocess.run(
            ['python', file_path], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        output = ""
        if result.stdout:
            output += f"Output:\n{result.stdout}"
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nExit code: {result.returncode}"
        
        return output or "No output produced"
        
    except subprocess.TimeoutExpired:
        return "❌ Execution timed out (10 seconds)"
    except Exception as e:
        return f"❌ Execution error: {str(e)}"

class CodeFixerAgent(BaseCodingAgent):
    """
    Version 2: Agent that can read, analyze, and fix buggy code
    
    Capabilities:
    - Read source code files
    - Identify bugs and issues
    - Fix the code
    - Execute and verify the fix
    """
    
    def __init__(self, llm_client):
        # Initialize with read, write, and execute tools
        tools = [
            Tool("read_file", "Read the contents of a file", read_file_tool),
            Tool("write_file", "Write content to a file", write_file_tool),
            Tool("execute_python", "Execute a Python file and return output", execute_python_tool)
        ]
        super().__init__(llm_client, tools)
    
    def fix_code(self, file_path: str, problem_description: str = None) -> str:
        """
        Fix bugs in a code file using the Read → Fix → Verify cycle
        
        Args:
            file_path: Path to the buggy code file
            problem_description: Optional description of the expected behavior
            
        Returns:
            Report of the fixing process
        """
        print(f"🔧 CodeFixer working on: {file_path}")
        
        # Step 1: Read the original code
        print("📖 Step 1: Reading the code...")
        file_result = self.execute_tool("read_file", file_path=file_path)
        
        if not file_result["success"]:
            return f"❌ Error reading file: {file_result['error']}"
        
        original_code = file_result["result"]
        print("✅ Code read successfully")
        
        # Step 2: Test the original code to see the problem
        print("🧪 Step 2: Testing original code...")
        original_output = self.execute_tool("execute_python", file_path=file_path)
        print("Original execution result:", original_output["result"][:200] + "..." if len(original_output["result"]) > 200 else original_output["result"])
        
        # Step 3: Analyze and fix the code
        print("🤔 Step 3: Analyzing and fixing...")
        
        problem_context = f"\nProblem description: {problem_description}" if problem_description else ""
        
        prompt = f"""You need to fix this buggy Python code:

{original_code}

Current execution result:
{original_output['result']}
{problem_context}

Please:
1. Identify what's wrong with the code
2. Provide the corrected version
3. Explain what you fixed

Return ONLY the corrected Python code, nothing else. The code should be complete and runnable."""

        fixed_code_response = self.think(prompt)
        
        # Extract just the code (simple approach - assumes LLM returns clean code)
        # In a more robust version, you'd parse this more carefully
        fixed_code = fixed_code_response.strip()
        
        # Step 4: Write the fixed code
        print("💾 Step 4: Writing fixed code...")
        write_result = self.execute_tool("write_file", file_path=file_path, content=fixed_code)
        
        if not write_result["success"]:
            return f"❌ Error writing fixed code: {write_result['error']}"
        
        # Step 5: Test the fixed code
        print("🧪 Step 5: Testing fixed code...")
        fixed_output = self.execute_tool("execute_python", file_path=file_path)
        
        # Step 6: Generate report
        report = f"""🔧 Code Fixing Report for {file_path}

📖 Original Code Issues:
{original_output['result']}

🛠️ Fix Applied:
{fixed_code_response}

✅ Fixed Code Result:
{fixed_output['result']}

Status: {'✅ SUCCESS' if fixed_output['success'] else '❌ STILL HAS ISSUES'}
"""
        
        print("🎉 Fixing process complete!")
        return report
    
    def quick_fix(self, code_snippet: str, expected_behavior: str) -> str:
        """
        Quick fix for a code snippet (without file I/O)
        Good for simple demonstrations
        
        Args:
            code_snippet: The buggy code as a string
            expected_behavior: What the code should do
            
        Returns:
            Fixed code with explanation
        """
        prompt = f"""Fix this buggy Python code:

```python
{code_snippet}
```

Expected behavior: {expected_behavior}

Please provide:
1. Explanation of the bug
2. The corrected code
3. Brief explanation of the fix

Keep it educational and clear for students."""
        
        return self.think(prompt)


# Simple testing functions
def create_sample_buggy_file():
    """Create a sample file with bugs for testing"""
    buggy_code = '''def calculate_area(radius):
    """Calculate the area of a circle"""
    return 3.14 * radius  # Bug: should be radius ** 2

def test_area():
    result = calculate_area(5)
    print(f"Area of circle with radius 5: {result}")
    print(f"Expected around 78.5, got: {result}")

if __name__ == "__main__":
    test_area()
'''
    
    with open('/tmp/buggy_circle.py', 'w') as f:
        f.write(buggy_code)
    
    return '/tmp/buggy_circle.py'

def test_code_fixer():
    """Simple test function to demonstrate CodeFixer capabilities"""
    print("🧪 Testing CodeFixer Agent...")
    
    # Create a mock LLM for testing
    class MockLLM:
        def complete(self, messages):
            # Mock response that fixes the circle area bug
            return '''def calculate_area(radius):
    """Calculate the area of a circle"""
    return 3.14 * radius ** 2  # Fixed: added ** 2

def test_area():
    result = calculate_area(5)
    print(f"Area of circle with radius 5: {result}")
    print(f"Expected around 78.5, got: {result}")

if __name__ == "__main__":
    test_area()'''
    
    agent = CodeFixerAgent(MockLLM())
    
    # Test quick fix
    buggy_snippet = "def add_numbers(a, b):\n    return a + b + 1  # Bug: extra +1"
    result = agent.quick_fix(buggy_snippet, "Should add two numbers without extra increment")
    
    print("✅ CodeFixer agent created successfully")
    print("Available tools:", list(agent.tools.keys()))
    print("\n📝 Quick fix demo result:")
    print(result[:200] + "..." if len(result) > 200 else result)

if __name__ == "__main__":
    test_code_fixer()
