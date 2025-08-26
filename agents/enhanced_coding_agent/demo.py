"""
Enhanced Coding Agent Demo

This script demonstrates the autonomous coding agent's capabilities:
- Iterative problem solving
- LLM-driven tool usage decisions
- Self-correction and improvement
- Comprehensive logging and analysis

Run this to see the enhanced agent in action!
"""

import sys
import os
from typing import Dict, Any

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'model-api'))

from agent import EnhancedCodingAgent
from examples.simple_problems import SIMPLE_PROBLEMS, get_problem, list_problems

# Import Gemini client (same as in original demo)
try:
    from dotenv import load_dotenv
    from google import genai
    load_dotenv()
except ImportError as e:
    print(f"⚠️  Missing dependencies for Gemini: {e}")
    print("Install with: pip install google-genai python-dotenv")

class GeminiLLMClient:
    """Gemini API client wrapper for the enhanced agent"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def complete(self, messages):
        """Complete a conversation using Gemini API"""
        try:
            # Convert messages to prompt for Gemini
            prompt_parts = []
            for message in messages:
                role = message.get("role", "")
                content = message.get("content", "")
                
                if role == "system":
                    prompt_parts.append(f"System Instructions: {content}")
                elif role == "user":
                    prompt_parts.append(f"User: {content}")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}")
            
            full_prompt = "\n\n".join(prompt_parts)
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

class MockLLMClient:
    """Mock LLM client for demonstration when API is not available"""
    
    def complete(self, messages):
        user_content = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_content += msg.get("content", "")
        
        # Mock responses for different types of requests
        if "ANALYSIS" in user_content and "APPROACH" in user_content:
            # This is a thinking request
            return self._mock_thinking_response(user_content)
        elif "def " in user_content or "python" in user_content.lower():
            # This is a code generation request
            return self._mock_code_response(user_content)
        else:
            return "Mock LLM response for demonstration purposes."
    
    def _mock_thinking_response(self, content):
        if "two_sum" in content.lower() or "two numbers" in content.lower():
            return """
ANALYSIS: This is a classic two-sum problem where we need to find two numbers in an array that add up to a target value and return their indices.

APPROACH: Use a hash map to store numbers we've seen and their indices. For each number, check if the complement (target - current_number) exists in the hash map.

PLAN:
1. Create an empty hash map to store number -> index mappings
2. Iterate through the array with indices
3. For each number, calculate complement = target - number
4. If complement exists in hash map, return [hash_map[complement], current_index]
5. Otherwise, store current number and index in hash map
6. Continue until solution found

PSEUDOCODE:
```
function two_sum(nums, target):
    num_map = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in num_map:
            return [num_map[complement], i]
        num_map[nums[i]] = i
    return []
```
"""
        else:
            return """
ANALYSIS: Need to understand the problem requirements and constraints.

APPROACH: Choose appropriate algorithm based on problem characteristics.

PLAN: Break down into logical steps.

PSEUDOCODE: Implement step by step solution.
"""
    
    def _mock_code_response(self, content):
        if "two_sum" in content.lower():
            return '''def two_sum(nums, target):
    """Find two numbers that add up to target and return their indices"""
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []

def run_tests():
    """Comprehensive test suite for two_sum function"""
    test_cases = [
        {
            "input": ([2, 7, 11, 15], 9),
            "expected": [0, 1],
            "description": "Basic case - first two elements"
        },
        {
            "input": ([3, 2, 4], 6),
            "expected": [1, 2],
            "description": "Middle elements"
        },
        {
            "input": ([3, 3], 6),
            "expected": [0, 1],
            "description": "Duplicate numbers"
        }
    ]
    
    print("=" * 60)
    print("TWO SUM SOLUTION TESTING REPORT")
    print("=" * 60)
    
    all_passed = True
    for i, test in enumerate(test_cases, 1):
        print(f"\\nTest Case {i}: {test['description']}")
        print(f"Input: {test['input']}")
        print(f"Expected: {test['expected']}")
        
        try:
            nums, target = test['input']
            actual = two_sum(nums, target)
            print(f"Actual: {actual}")
            
            if actual == test['expected']:
                print("✅ PASSED")
            else:
                print("❌ FAILED")
                all_passed = False
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
            all_passed = False
    
    print(f"\\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    run_tests()'''
        else:
            return '''def solution_function(params):
    """Generated solution function"""
    # Mock implementation
    return params

def run_tests():
    """Mock test function"""
    print("Mock test execution")
    return True

if __name__ == "__main__":
    run_tests()'''

def get_llm_client():
    """Get LLM client (Gemini or Mock)"""
    try:
        client = GeminiLLMClient()
        print("✅ Using Gemini LLM client")
        return client
    except Exception as e:
        print(f"⚠️  Could not initialize Gemini client: {e}")
        print("📝 Using mock client for demonstration")
        return MockLLMClient()

def demo_problem_solving():
    """Demonstrate the agent solving a programming problem"""
    print("🤖 Enhanced Coding Agent Demo")
    print("=" * 50)
    
    # Initialize the agent
    llm_client = get_llm_client()
    workspace_path = os.path.join(os.path.dirname(__file__), "workspace")
    agent = EnhancedCodingAgent(llm_client, workspace_path, max_iterations=3)
    
    print(f"🏗️  Agent initialized with workspace: {workspace_path}")
    print(f"🔧 Available tools: {list(agent.tools.keys())}")
    
    # Choose a problem to solve
    print("\\n📚 Available problems:")
    for i, (key, problem) in enumerate(SIMPLE_PROBLEMS.items(), 1):
        print(f"  {i}. {problem['title']} ({problem['difficulty']})")
    
    try:
        choice = input("\\nChoose a problem (1-5) or press Enter for Two Sum: ").strip()
        if choice and choice.isdigit() and 1 <= int(choice) <= 5:
            problem_key = list(SIMPLE_PROBLEMS.keys())[int(choice) - 1]
        else:
            problem_key = "two_sum"
        
        problem = SIMPLE_PROBLEMS[problem_key]
        print(f"\\n🎯 Selected: {problem['title']}")
        print(f"📋 Description: {problem['description']}")
        
        # Solve the problem
        print("\\n🚀 Starting autonomous problem solving...")
        result = agent.solve_problem(problem['description'])
        
        # Display results
        print("\\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        
        if result['success']:
            print("✅ SUCCESS! Problem solved successfully!")
            print(f"🔄 Iterations used: {result['total_iterations']}/{result['max_iterations']}")
            
            best_solution = result['best_solution']
            if best_solution and 'filename' in best_solution:
                print(f"💾 Solution saved as: {best_solution['filename']}")
                
                # Try to show the generated code
                try:
                    solution_path = os.path.join(workspace_path, "solutions", best_solution['filename'])
                    if os.path.exists(solution_path):
                        print("\\n📝 Generated solution:")
                        print("-" * 40)
                        with open(solution_path, 'r') as f:
                            print(f.read())
                except Exception as e:
                    print(f"Could not display solution: {e}")
        else:
            print("❌ FAILED to solve the problem")
            print(f"🔄 Iterations attempted: {result['total_iterations']}/{result['max_iterations']}")
            
            print("\\n🔍 Attempt summary:")
            for i, attempt in enumerate(result['attempts'], 1):
                status = "✅" if attempt.get('success', False) else "❌"
                print(f"  {status} Iteration {i}: {attempt.get('status', 'unknown')}")
        
        print(f"\\n📁 Check workspace for all files: {workspace_path}")
        
    except KeyboardInterrupt:
        print("\\n\\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\\n❌ Demo error: {e}")

def demo_workspace_exploration():
    """Show the workspace contents after a run"""
    workspace_path = os.path.join(os.path.dirname(__file__), "workspace")
    
    print("\\n🗂️  Workspace Exploration")
    print("=" * 40)
    
    try:
        # Show solutions
        solutions_dir = os.path.join(workspace_path, "solutions")
        if os.path.exists(solutions_dir):
            solutions = [f for f in os.listdir(solutions_dir) if f.endswith('.py')]
            print(f"📄 Solution files ({len(solutions)}):")
            for solution in solutions:
                print(f"  - {solution}")
        
        # Show logs
        logs_dir = os.path.join(workspace_path, "logs") 
        if os.path.exists(logs_dir):
            logs = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
            print(f"\\n📋 Execution logs ({len(logs)}):")
            for log in logs[-3:]:  # Show last 3 logs
                print(f"  - {log}")
    
    except Exception as e:
        print(f"Error exploring workspace: {e}")

def interactive_demo():
    """Interactive demo where users can input their own problems"""
    print("\\n🎮 Interactive Mode")
    print("=" * 40)
    print("Enter your own programming problem for the agent to solve!")
    print("(Type 'quit' to exit)")
    
    llm_client = get_llm_client()
    workspace_path = os.path.join(os.path.dirname(__file__), "workspace")
    agent = EnhancedCodingAgent(llm_client, workspace_path, max_iterations=3)
    
    while True:
        try:
            print("\\nEnter your problem statement:")
            problem = input("> ").strip()
            
            if problem.lower() in ['quit', 'exit', 'q']:
                print("👋 Exiting interactive mode")
                break
            
            if len(problem) < 20:
                print("⚠️  Please provide a more detailed problem description")
                continue
            
            print(f"\\n🤖 Agent working on: {problem[:60]}...")
            result = agent.solve_problem(problem)
            
            if result['success']:
                print("✅ Problem solved! Check the workspace for results.")
            else:
                print("❌ Agent couldn't solve this problem. Check logs for details.")
                
        except KeyboardInterrupt:
            print("\\n👋 Interactive mode interrupted")
            break

def main():
    """Main demo function"""
    print("🎯 Enhanced Coding Agent Demo Options:")
    print("1. Automated demo with predefined problems")
    print("2. Interactive mode (enter your own problems)")
    print("3. Explore workspace from previous runs")
    
    try:
        choice = input("\\nChoose option (1-3) or press Enter for option 1: ").strip()
        
        if choice == "2":
            interactive_demo()
        elif choice == "3":
            demo_workspace_exploration()
        else:
            demo_problem_solving()
            
    except KeyboardInterrupt:
        print("\\n\\n👋 Demo ended by user")

if __name__ == "__main__":
    main()
