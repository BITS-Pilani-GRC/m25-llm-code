"""
Thinking Tool - LLM-based reasoning and planning

This tool uses the LLM to analyze problems, create plans, and generate pseudocode
before actual code implementation.
"""

from typing import Dict, Any, List, Optional
from .base_tool import BaseTool

class ThinkingTool(BaseTool):
    """
    Uses LLM to think through problems and create implementation plans
    
    This tool helps the agent:
    - Understand the problem requirements
    - Break down complex problems
    - Plan the solution approach
    - Learn from previous failed attempts
    """
    
    def __init__(self, llm_client):
        super().__init__("think")
        self.llm_client = llm_client
    
    def execute(self, problem_statement: str, previous_attempts: Optional[List[str]] = None, 
                context: Optional[str] = None) -> Dict[str, Any]:
        """
        Think through a programming problem and create a plan
        
        Args:
            problem_statement: The coding problem to solve
            previous_attempts: List of previous failed attempts (for learning)
            context: Additional context or constraints
            
        Returns:
            Dict with thinking process, plan, and pseudocode
        """
        try:
            prompt = self._build_thinking_prompt(problem_statement, previous_attempts, context)
            
            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            
            thinking_response = self.llm_client.complete(messages)
            
            return self.format_result(
                success=True,
                result={
                    "thinking_process": thinking_response,
                    "problem_analysis": self._extract_problem_analysis(thinking_response),
                    "solution_plan": self._extract_solution_plan(thinking_response),
                    "pseudocode": self._extract_pseudocode(thinking_response)
                }
            )
            
        except Exception as e:
            return self.format_result(success=False, error=f"Thinking tool error: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """System prompt that defines the thinking tool's role"""
        return """You are a programming problem analysis expert. Your job is to think through coding problems systematically.

When given a problem:
1. ANALYZE the requirements carefully
2. IDENTIFY the key constraints and edge cases  
3. CHOOSE the best algorithmic approach
4. CREATE a step-by-step plan
5. WRITE clear pseudocode

Be thorough but concise. Focus on logical reasoning and clear planning.
Structure your response with clear sections: ANALYSIS, APPROACH, PLAN, PSEUDOCODE."""
    
    def _build_thinking_prompt(self, problem_statement: str, previous_attempts: Optional[List[str]], 
                             context: Optional[str]) -> str:
        """Build the complete prompt for thinking"""
        prompt = f"""PROBLEM TO SOLVE:
{problem_statement}

"""
        
        if context:
            prompt += f"""ADDITIONAL CONTEXT:
{context}

"""
        
        if previous_attempts:
            prompt += f"""PREVIOUS FAILED ATTEMPTS:
{chr(10).join(f'Attempt {i+1}: {attempt}' for i, attempt in enumerate(previous_attempts))}

Please learn from these failures and think of a better approach.

"""
        
        prompt += """Please think through this problem systematically:

1. ANALYSIS: What exactly does this problem ask for? What are the inputs, outputs, constraints?

2. APPROACH: What algorithmic approach would work best? Consider time/space complexity.

3. PLAN: Break down the solution into clear steps.

4. PSEUDOCODE: Write clear pseudocode for the solution.

Be specific and detailed in your thinking process."""
        
        return prompt
    
    def _extract_problem_analysis(self, response: str) -> str:
        """Extract the problem analysis section"""
        return self._extract_section(response, "ANALYSIS")
    
    def _extract_solution_plan(self, response: str) -> str:
        """Extract the solution plan section"""
        return self._extract_section(response, "PLAN")
    
    def _extract_pseudocode(self, response: str) -> str:
        """Extract the pseudocode section"""
        return self._extract_section(response, "PSEUDOCODE")
    
    def _extract_section(self, response: str, section_name: str) -> str:
        """Helper to extract specific sections from the response"""
        lines = response.split('\n')
        in_section = False
        section_content = []
        
        for line in lines:
            if section_name.upper() in line.upper() and ':' in line:
                in_section = True
                continue
            elif in_section and any(keyword in line.upper() for keyword in ['ANALYSIS', 'APPROACH', 'PLAN', 'PSEUDOCODE']) and ':' in line:
                break
            elif in_section:
                section_content.append(line)
        
        return '\n'.join(section_content).strip()
    
    def get_description(self) -> str:
        return "Analyze programming problems and create detailed implementation plans using logical reasoning"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "think",
                "description": self.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem_statement": {
                            "type": "string",
                            "description": "The programming problem to analyze and plan for"
                        },
                        "previous_attempts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional list of previous failed attempts to learn from"
                        },
                        "context": {
                            "type": "string", 
                            "description": "Optional additional context or constraints"
                        }
                    },
                    "required": ["problem_statement"]
                }
            }
        }
