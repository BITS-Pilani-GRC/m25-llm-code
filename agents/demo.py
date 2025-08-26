"""
Coding Agent Demo - Educational demonstration for LLM class

This script demonstrates two versions of coding agents:
- Version 1: Code Reader (Analysis)
- Version 2: Code Fixer (Correction)

Students can run this to see agents in action and experiment with different examples.
"""

import sys
import os

# Add the model-api directory to path to import LLM clients
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model-api'))

from v1_code_reader import CodeReaderAgent
from v2_code_fixer import CodeFixerAgent

# Import Gemini API components
try:
    from dotenv import load_dotenv
    from google import genai
    load_dotenv()
except ImportError as e:
    print(f"⚠️  Missing dependencies for Gemini: {e}")
    print("Install with: pip install google-genai python-dotenv")

class GeminiLLMClient:
    """
    Gemini API client wrapper for coding agents
    Implements the same interface as other LLM clients (complete method)
    """
    
    def __init__(self):
        # Get API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def complete(self, messages):
        """
        Complete a conversation using Gemini API
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            
        Returns:
            String response from Gemini
        """
        try:
            # Convert messages to a single prompt for Gemini
            # Gemini expects a single content string, so we'll format the conversation
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
            
            # Join all parts into a single prompt
            full_prompt = "\n\n".join(prompt_parts)
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

def get_llm_client():
    """
    Get an LLM client for the demo
    Students can modify this to use different LLM providers
    """
    try:
        # Try to import and use Gemini client
        client = GeminiLLMClient()
        print("✅ Using Gemini client")
        return client
    except Exception as e:
        print(f"⚠️  Could not initialize Gemini client: {e}")
        print("📝 Using mock client for demonstration")
        return MockLLMClient()

class MockLLMClient:
    """
    Simple mock LLM client for demonstration when real LLM is not available
    Students can see the structure even without API keys
    """
    
    def complete(self, messages):
        # Extract the user's question/prompt
        user_message = ""
        for msg in messages:
            if msg["role"] == "user":
                user_message = msg["content"]
        
        # Simple pattern matching for common demo scenarios
        if "mystery_function" in user_message.lower():
            return """This code defines a mathematical function that calculates x*y + x.

For mystery_function(3, 4):
- First: 3 * 4 = 12
- Then: 12 + 3 = 15
- Result: 15

This is essentially calculating x * (y + 1). It's a linear function with a multiplicative factor."""

        elif "circle area" in user_message.lower() and "bug" in user_message.lower():
            return """def calculate_circle_area(radius):
    \"\"\"Calculate the area of a circle\"\"\"
    return 3.14159 * radius ** 2  # Fixed: added ** 2 for radius squared"""

        elif "bug" in user_message.lower() or "fix" in user_message.lower():
            return """I can see there's a bug in this code. The issue appears to be in the mathematical calculation. Here's the corrected version:

[Fixed code would be provided here based on the specific bug identified]

The main issue was [explanation of the bug and how it was fixed]."""

        else:
            return """This code appears to be a well-structured function that performs [specific operation]. 

Key components:
1. Input validation
2. Main processing logic  
3. Return appropriate result

The code follows good Python practices and should work correctly for its intended purpose."""

def demo_version_1():
    """Demonstrate Version 1: Code Reader Agent"""
    print("\n" + "="*60)
    print("🔍 DEMO: Version 1 - Code Reader Agent")
    print("="*60)
    print("Purpose: Show how LLM can read and understand code")
    print()
    
    # Initialize agent
    llm_client = get_llm_client()
    agent = CodeReaderAgent(llm_client)
    
    # Demo 1: Analyze a mysterious function
    print("📋 Demo 1: Analyzing a mysterious function")
    print("-" * 40)
    
    example_file = "examples/simple_function.py"
    if os.path.exists(example_file):
        analysis = agent.analyze_code(
            example_file, 
            "What does the mystery_function do? What would it return for mystery_function(3, 4)?"
        )
        print("🤖 Agent Analysis:")
        print(analysis)
        print()
    else:
        print(f"⚠️  Example file {example_file} not found")
    
    # Demo 2: General code analysis
    print("📋 Demo 2: General code structure analysis")
    print("-" * 40)
    
    string_file = "examples/string_processor.py"
    if os.path.exists(string_file):
        analysis = agent.analyze_code(string_file)
        print("🤖 Agent Analysis:")
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        print()
    else:
        print(f"⚠️  Example file {string_file} not found")

def demo_version_2():
    """Demonstrate Version 2: Code Fixer Agent"""
    print("\n" + "="*60)
    print("🔧 DEMO: Version 2 - Code Fixer Agent")
    print("="*60)
    print("Purpose: Show how LLM can identify and fix bugs")
    print()
    
    # Initialize agent
    llm_client = get_llm_client()
    agent = CodeFixerAgent(llm_client)
    
    # Demo 1: Quick fix demonstration
    print("📋 Demo 1: Quick fix for simple bug")
    print("-" * 40)
    
    buggy_code = """def calculate_total(items):
    total = 0
    for item in items:
        total += item + 1  # Bug: extra +1 added
    return total"""
    
    result = agent.quick_fix(
        buggy_code, 
        "Should calculate the sum of all items in the list without any extra addition"
    )
    print("🤖 Agent Fix:")
    print(result)
    print()
    
    # Demo 2: File-based fixing (if example file exists)
    print("📋 Demo 2: Fixing bugs in a file")
    print("-" * 40)
    
    buggy_file = "examples/buggy_math.py"
    if os.path.exists(buggy_file):
        # Make a copy to fix so we don't modify the original
        import shutil
        temp_file = "examples/buggy_math_temp.py"
        shutil.copy(buggy_file, temp_file)
        
        try:
            report = agent.fix_code(
                temp_file,
                "The circle area function should return πr² (pi times radius squared)"
            )
            print("🤖 Agent Fixing Report:")
            print(report[:800] + "..." if len(report) > 800 else report)
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            print(f"⚠️  Demo error: {e}")
            print("This is normal when using mock LLM - shows the process flow")
    else:
        print(f"⚠️  Example file {buggy_file} not found")

def run_interactive_demo():
    """Interactive demo where students can experiment"""
    print("\n" + "="*60)
    print("🎮 INTERACTIVE DEMO")
    print("="*60)
    print("Try the agents yourself! (Type 'quit' to exit)")
    print()
    
    llm_client = get_llm_client()
    reader_agent = CodeReaderAgent(llm_client)
    fixer_agent = CodeFixerAgent(llm_client)
    
    while True:
        print("\nChoose an option:")
        print("1. Analyze code (Code Reader)")
        print("2. Fix code snippet (Code Fixer)")
        print("3. List example files")
        print("4. Quit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            file_path = input("Enter file path to analyze: ").strip()
            if os.path.exists(file_path):
                question = input("Any specific question about the code? (or press Enter): ").strip()
                question = question if question else None
                result = reader_agent.analyze_code(file_path, question)
                print("\n🤖 Analysis:")
                print(result)
            else:
                print(f"❌ File not found: {file_path}")
        
        elif choice == "2":
            print("Enter your buggy code (end with a line containing only 'END'):")
            code_lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                code_lines.append(line)
            
            code = "\n".join(code_lines)
            expected = input("What should this code do? ").strip()
            
            result = fixer_agent.quick_fix(code, expected)
            print("\n🤖 Fix:")
            print(result)
        
        elif choice == "3":
            print("\nAvailable example files:")
            examples_dir = "examples"
            if os.path.exists(examples_dir):
                for file in os.listdir(examples_dir):
                    if file.endswith('.py'):
                        print(f"  - examples/{file}")
            else:
                print("  No examples directory found")
        
        elif choice == "4" or choice.lower() == "quit":
            print("👋 Thanks for trying the coding agents demo!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main demo function"""
    print("🤖 Welcome to the Coding Agent Demo!")
    print("This demonstrates LLM-powered coding agents for educational purposes.")
    print()
    print("What you'll see:")
    print("• Version 1: How agents can read and understand code")
    print("• Version 2: How agents can identify and fix bugs")
    print("• Interactive mode to experiment yourself")
    
    try:
        # Run Version 1 demo
        demo_version_1()
        
        # Run Version 2 demo  
        demo_version_2()
        
        # Interactive demo
        print("\n🎯 Ready for interactive demo?")
        if input("Press Enter to continue or 'skip' to exit: ").strip().lower() != 'skip':
            run_interactive_demo()
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying it!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("This helps students understand error handling in agents!")

if __name__ == "__main__":
    main()
