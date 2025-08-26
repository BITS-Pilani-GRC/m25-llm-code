"""
Code Generation Tool - LLM-based code generation with comprehensive tests

This tool generates complete, self-contained Python scripts with:
- Solution implementation
- Comprehensive test cases
- Clear output formatting
- Error handling
"""

from typing import Dict, Any, Optional
from .base_tool import BaseTool

class CodeGenerationTool(BaseTool):
    """
    Generates complete Python solutions with comprehensive testing
    
    Creates self-contained scripts that include:
    - The main solution function(s)
    - Multiple test cases with edge cases
    - Clear execution and reporting
    - Proper error handling
    """
    
    def __init__(self, llm_client):
        super().__init__("generate_code")
        self.llm_client = llm_client
    
    def execute(self, problem_statement: str, thinking_output: str, 
                previous_code: Optional[str] = None, 
                execution_feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate complete Python solution with tests
        
        Args:
            problem_statement: Original problem description
            thinking_output: Result from thinking tool
            previous_code: Previous code attempt (for improvements)
            execution_feedback: Feedback from previous execution
            
        Returns:
            Dict with generated code and metadata
        """
        try:
            prompt = self._build_code_generation_prompt(
                problem_statement, thinking_output, previous_code, execution_feedback
            )
            
            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            
            code_response = self.llm_client.complete(messages)
            
            # Extract just the Python code from the response
            python_code = self._extract_python_code(code_response)
            
            return self.format_result(
                success=True,
                result={
                    "generated_code": python_code,
                    "full_response": code_response,
                    "code_structure": self._analyze_code_structure(python_code)
                }
            )
            
        except Exception as e:
            return self.format_result(success=False, error=f"Code generation error: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """System prompt for code generation"""
        return """You are an expert Python programmer. Generate complete, working Python solutions.

REQUIREMENTS:
1. Create a self-contained Python script
2. Include the main solution function(s)
3. Add comprehensive test cases (at least 5-7 test cases including edge cases)
4. Include a run_tests() function that executes all tests
5. Format output clearly: show input, expected output, actual output, and pass/fail status
6. Handle errors gracefully
7. Include a main block that runs the tests when script is executed

CODE STRUCTURE:
```python
def solution_function(params):
    \"\"\"Main solution with clear docstring\"\"\"
    # Implementation here
    pass

def run_tests():
    \"\"\"Comprehensive test suite\"\"\"
    # Test cases with clear reporting
    pass

if __name__ == "__main__":
    run_tests()
```

IMPORTANT: Return ONLY the Python code, no explanations or markdown formatting."""
    
    def _build_code_generation_prompt(self, problem_statement: str, thinking_output: str,
                                    previous_code: Optional[str], execution_feedback: Optional[str]) -> str:
        """Build the complete prompt for code generation"""
        prompt = f"""PROBLEM STATEMENT:
{problem_statement}

THINKING AND PLANNING:
{thinking_output}

"""
        
        if previous_code and execution_feedback:
            prompt += f"""PREVIOUS CODE ATTEMPT:
{previous_code}

EXECUTION FEEDBACK:
{execution_feedback}

Please improve the code based on this feedback.

"""
        
        prompt += """Generate a complete Python solution that:

1. Implements the solution based on the thinking/planning above
2. Includes comprehensive test cases covering:
   - Normal cases
   - Edge cases  
   - Error conditions
   - Boundary values
3. Has clear, readable output showing test results
4. Is completely self-contained and runnable

Remember: Return ONLY the Python code, no markdown or explanations."""
        
        return prompt
    
    def _extract_python_code(self, response: str) -> str:
        """Extract clean Python code from LLM response"""
        lines = response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            # Handle markdown code blocks
            if line.strip().startswith('```python'):
                in_code_block = True
                continue
            elif line.strip() == '```' and in_code_block:
                break
            elif in_code_block or (not line.strip().startswith('```') and 'def ' in line):
                # We're in a code block or found function definition
                in_code_block = True
                code_lines.append(line)
            elif in_code_block:
                code_lines.append(line)
        
        # If no code block markers found, assume entire response is code
        if not code_lines and 'def ' in response:
            code_lines = lines
        
        return '\n'.join(code_lines).strip()
    
    def _analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """Analyze the structure of generated code"""
        analysis = {
            "has_solution_function": False,
            "has_test_function": False,
            "has_main_block": False,
            "function_count": 0,
            "estimated_test_cases": 0
        }
        
        lines = code.split('\n')
        for line in lines:
            if line.strip().startswith('def '):
                analysis["function_count"] += 1
                if 'test' in line.lower():
                    analysis["has_test_function"] = True
                else:
                    analysis["has_solution_function"] = True
            elif line.strip().startswith('if __name__'):
                analysis["has_main_block"] = True
            elif 'assert' in line or 'test_cases' in line.lower():
                analysis["estimated_test_cases"] += 1
        
        return analysis
    
    def get_description(self) -> str:
        return "Generate complete Python solutions with comprehensive test cases and clear output formatting"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function", 
            "function": {
                "name": "generate_code",
                "description": self.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem_statement": {
                            "type": "string",
                            "description": "The original programming problem to solve"
                        },
                        "thinking_output": {
                            "type": "string",
                            "description": "The analysis and plan from the thinking tool"
                        },
                        "previous_code": {
                            "type": "string",
                            "description": "Optional previous code attempt to improve upon"
                        },
                        "execution_feedback": {
                            "type": "string",
                            "description": "Optional feedback from previous code execution"
                        }
                    },
                    "required": ["problem_statement", "thinking_output"]
                }
            }
        }
