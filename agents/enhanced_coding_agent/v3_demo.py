"""
Fully Autonomous Coding Agent Demo (Version 3)

This demo showcases the V3 agent's complete autonomy:
- LLM decides all tool usage
- No hardcoded workflows  
- Dynamic adaptation to problems
- Self-regulated stopping
- Creative problem-solving approaches

Compare this to V2 to see the difference between structured and autonomous AI.
"""

import sys
import os
import json
from typing import Dict, Any

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'model-api'))

from v3_autonomous_agent import FullyAutonomousCodingAgent
from examples.simple_problems import SIMPLE_PROBLEMS, get_problem, list_problems

# Import Gemini client (same as other demos)
try:
    from dotenv import load_dotenv
    from google import genai
    load_dotenv()
except ImportError as e:
    print(f"⚠️  Missing dependencies for Gemini: {e}")
    print("Install with: pip install google-genai python-dotenv")

class GeminiLLMClient:
    """Gemini API client wrapper"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
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

class MockAutonomousLLM:
    """Enhanced mock LLM that simulates autonomous decision-making"""
    
    def __init__(self):
        self.call_count = 0
        self.decision_patterns = self._init_decision_patterns()
    
    def complete(self, messages):
        """Mock autonomous LLM responses"""
        self.call_count += 1
        
        # Extract the prompt content
        user_content = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_content += msg.get("content", "")
        
        # Determine response type and generate appropriate mock decision
        if "AUTONOMOUS DECISION REQUIRED" in user_content:
            return self._generate_autonomous_decision(user_content)
        else:
            return self._generate_tool_response(user_content)
    
    def _generate_autonomous_decision(self, content: str) -> str:
        """Generate mock autonomous decisions based on context"""
        
        # Analyze the context to make realistic decisions
        tool_calls_used = self._extract_number(content, "Tool calls used:")
        files_created = self._extract_number(content, "Files created:")
        executions = self._extract_number(content, "Code executions:")
        quality_score = self._extract_number(content, "Best quality score:")
        
        # Decision logic based on current state
        if tool_calls_used == 0:
            # First call - always think
            return '''
{
    "action": "use_tool",
    "tool": "think",
    "parameters": {
        "focus": "problem analysis",
        "context": "Initial problem understanding"
    },
    "reasoning": "I need to start by understanding the problem requirements and planning my approach."
}'''
        
        elif files_created == 0 and tool_calls_used >= 1:
            # After thinking, generate code
            return '''
{
    "action": "use_tool",
    "tool": "generate_code",
    "parameters": {
        "approach": "initial solution",
        "based_on": "problem analysis"
    },
    "reasoning": "Based on my analysis, I'll generate an initial solution with comprehensive tests."
}'''
        
        elif files_created >= 1 and executions == 0:
            # After generating, write file
            return '''
{
    "action": "use_tool",
    "tool": "write_file",
    "parameters": {
        "filename": "solution_v1.py",
        "content": "# Generated solution would be here",
        "type": "solution"
    },
    "reasoning": "I need to save the generated solution so I can test it."
}'''
        
        elif files_created >= 1 and executions == 0 and "solution" in content:
            # Execute the solution
            return '''
{
    "action": "use_tool",
    "tool": "execute_code",
    "parameters": {
        "filename": "solution_v1.py",
        "goal": "test initial solution"
    },
    "reasoning": "Time to execute and test my solution to see how well it works."
}'''
        
        elif quality_score >= 80:
            # High quality - stop
            return '''
{
    "action": "stop",
    "reasoning": "The solution has achieved high quality (80+/100) with good test coverage. I'm satisfied with this result."
}'''
        
        elif quality_score > 0 and quality_score < 70:
            # Low quality - think about improvements
            return '''
{
    "action": "use_tool",
    "tool": "think",
    "parameters": {
        "focus": "solution improvement",
        "context": "Analyzing test failures and quality issues"
    },
    "reasoning": "The current solution quality is below acceptable levels. I need to analyze what went wrong and plan improvements."
}'''
        
        elif tool_calls_used >= 12:
            # Running out of calls - stop
            return '''
{
    "action": "stop",
    "reasoning": "I'm approaching the tool call limit. The current solution is functional and I should finalize it."
}'''
        
        else:
            # Default: improve the solution
            return '''
{
    "action": "use_tool",
    "tool": "generate_code",
    "parameters": {
        "approach": "improved solution",
        "based_on": "previous execution results"
    },
    "reasoning": "I'll generate an improved version of the solution based on the execution feedback."
}'''
    
    def _generate_tool_response(self, content: str) -> str:
        """Generate responses for tool execution"""
        if "think" in content.lower() and "two sum" in content.lower():
            return """
ANALYSIS: This is a classic two-sum problem requiring finding two numbers that add up to a target.

APPROACH: Use a hash map to store seen numbers and their indices for O(n) time complexity.

PLAN:
1. Create empty hash map
2. Iterate through array
3. Check if complement exists
4. Return indices if found

PSEUDOCODE:
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
"""
        else:
            return "Mock tool response for demonstration purposes."
    
    def _extract_number(self, text: str, pattern: str) -> int:
        """Extract number following a pattern in text"""
        try:
            start = text.find(pattern)
            if start == -1:
                return 0
            
            # Find the number after the pattern
            start += len(pattern)
            end = start
            while end < len(text) and (text[end].isdigit() or text[end] == '.'):
                end += 1
            
            if start < end:
                return int(float(text[start:end]))
        except:
            pass
        return 0
    
    def _init_decision_patterns(self):
        """Initialize decision patterns for more realistic behavior"""
        return {
            "think_first": True,
            "generate_after_think": True,
            "execute_after_generate": True,
            "improve_on_failure": True,
            "stop_on_success": True
        }

def get_llm_client():
    """Get LLM client (Gemini or Mock)"""
    try:
        client = GeminiLLMClient()
        print("✅ Using Gemini LLM client for autonomous decisions")
        return client
    except Exception as e:
        print(f"⚠️  Could not initialize Gemini client: {e}")
        print("📝 Using mock autonomous LLM for demonstration")
        return MockAutonomousLLM()

def demonstrate_autonomous_behavior():
    """Show the difference between V2 (structured) and V3 (autonomous)"""
    print("🎯 Autonomous vs Structured Agent Comparison")
    print("=" * 60)
    
    print("📋 V2 Enhanced Agent (Structured):")
    print("  1. think() → 2. generate_code() → 3. write_file() →")
    print("  4. execute_code() → 5. evaluate() → REPEAT")
    print("  ❌ Fixed workflow, predictable sequence")
    
    print("\n🤖 V3 Autonomous Agent (Dynamic):")
    print("  LLM decides: What should I do next?")
    print("  ✅ Completely flexible workflow")
    print("  ✅ Context-aware decisions")
    print("  ✅ Creative problem-solving")
    print("  ✅ Self-regulated stopping")
    
    print("\n🔄 Example V3 Decision Flows:")
    print("Flow A: think → think → generate_code → write_file → execute_code → STOP")
    print("Flow B: think → generate_code → write_file → execute_code → read_file → think → generate_code → STOP")
    print("Flow C: think → generate_code → write_file → execute_code → execute_code → think → STOP")

def demo_autonomous_problem_solving():
    """Main demo showing autonomous problem solving"""
    print("\n🚀 Fully Autonomous Coding Agent Demo")
    print("=" * 60)
    
    # Initialize the autonomous agent
    llm_client = get_llm_client()
    workspace_path = os.path.join(os.path.dirname(__file__), "workspace_v3")
    agent = FullyAutonomousCodingAgent(
        llm_client=llm_client,
        workspace_path=workspace_path,
        max_tool_calls=15,
        verbose=True
    )
    
    print(f"\n{agent.get_capabilities_summary()}")
    
    # Choose a problem
    print("\n📚 Available Problems:")
    for i, (key, problem) in enumerate(SIMPLE_PROBLEMS.items(), 1):
        print(f"  {i}. {problem['title']} ({problem['difficulty']})")
    
    try:
        choice = input("\nChoose a problem (1-5) or press Enter for Two Sum: ").strip()
        if choice and choice.isdigit() and 1 <= int(choice) <= 5:
            problem_key = list(SIMPLE_PROBLEMS.keys())[int(choice) - 1]
        else:
            problem_key = "two_sum"
        
        problem = SIMPLE_PROBLEMS[problem_key]
        print(f"\n🎯 Selected: {problem['title']}")
        print(f"📋 Problem: {problem['description']}")
        
        print("\n" + "="*80)
        print("🤖 AUTONOMOUS AGENT SESSION STARTING")
        print("="*80)
        print("Watch as the agent makes completely autonomous decisions...")
        print("No hardcoded workflow - pure LLM reasoning!")
        print()
        
        # Solve autonomously
        result = agent.solve_problem(problem['description'])
        
        # Show results
        print("\n" + "="*80)
        print("📊 AUTONOMOUS SESSION RESULTS")
        print("="*80)
        
        session_info = result['session_info']
        results = result['results']
        activity = result['activity_summary']
        
        print(f"🎯 Status: {session_info['completion_status']}")
        print(f"⏱️ Duration: {session_info['session_duration']:.1f} seconds")
        print(f"🔧 Tool Calls: {session_info['total_tool_calls']}/{session_info['max_tool_calls']}")
        print(f"🎖️ Quality Score: {results['best_quality_score']}/100")
        print(f"😊 Satisfaction: {results['satisfaction_level']}/100")
        print(f"🤝 Confidence: {results['confidence_level']}/100")
        
        print(f"\n📊 Activity Summary:")
        print(f"  - Files created: {activity['files_created']}")
        print(f"  - Code executions: {activity['code_executions']}")
        print(f"  - Thinking sessions: {activity['thinking_sessions']}")
        print(f"  - Issues identified: {activity['issues_identified']}")
        
        # Show decision trail
        print(f"\n🧠 Autonomous Decision Trail:")
        for i, decision in enumerate(result['decision_trail'], 1):
            status = "✅" if decision['success'] else "❌"
            print(f"  {i}. {status} {decision['tool']}: {decision['reasoning'][:60]}...")
        
        print(f"\n🛑 Stop Reason: {results['stop_reason']}")
        
        # Show workspace artifacts
        if result['workspace_artifacts']['files']:
            print(f"\n📁 Generated Files:")
            for file_info in result['workspace_artifacts']['files']:
                print(f"  - {file_info['filename']} ({file_info['type']}, {file_info['size']} chars)")
        
        print(f"\n📂 Full workspace: {workspace_path}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

def compare_agent_versions():
    """Show a side-by-side comparison of agent capabilities"""
    print("\n📊 Agent Version Comparison")
    print("=" * 80)
    
    comparison = [
        ("Feature", "V1 Reader", "V2 Enhanced", "V3 Autonomous"),
        ("---", "---", "---", "---"),
        ("Decision Making", "Human", "Structured", "Fully LLM-driven"),
        ("Workflow", "Manual", "Hardcoded", "Dynamic"),
        ("Tool Selection", "Predetermined", "Sequential", "Context-aware"),
        ("Adaptation", "None", "Limited", "Complete"),
        ("Creativity", "Low", "Medium", "High"),
        ("Stopping Logic", "Manual", "Rule-based", "Self-determined"),
        ("Learning", "None", "Basic", "Adaptive"),
        ("Autonomy Level", "10%", "60%", "95%"),
        ("Real-world Similarity", "Low", "Medium", "High")
    ]
    
    for row in comparison:
        print(f"{row[0]:<20} | {row[1]:<12} | {row[2]:<12} | {row[3]:<15}")

def explore_workspace():
    """Explore the workspace to see autonomous agent artifacts"""
    workspace_path = os.path.join(os.path.dirname(__file__), "workspace_v3")
    
    print("\n🗂️ Autonomous Agent Workspace Explorer")
    print("=" * 50)
    
    if not os.path.exists(workspace_path):
        print("No workspace found. Run the autonomous demo first!")
        return
    
    # Show directory structure
    print(f"📂 Workspace: {workspace_path}")
    
    try:
        for root, dirs, files in os.walk(workspace_path):
            level = root.replace(workspace_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
        # Show recent session reports
        logs_dir = os.path.join(workspace_path, "logs")
        if os.path.exists(logs_dir):
            reports = [f for f in os.listdir(logs_dir) if f.startswith("session_report_")]
            if reports:
                latest_report = max(reports)
                print(f"\n📋 Latest Session Report: {latest_report}")
                
                try:
                    with open(os.path.join(logs_dir, latest_report), 'r') as f:
                        report = json.load(f)
                    
                    print(f"   Problem: {report['session_info']['problem_statement'][:60]}...")
                    print(f"   Status: {report['session_info']['completion_status']}")
                    print(f"   Tool Calls: {report['session_info']['total_tool_calls']}")
                    print(f"   Quality: {report['results']['best_quality_score']}/100")
                    
                except Exception as e:
                    print(f"   Could not read report: {e}")
    
    except Exception as e:
        print(f"Error exploring workspace: {e}")

def main():
    """Main demo function"""
    print("🤖 Fully Autonomous Coding Agent (V3) Demo")
    print("Demonstrating true AI autonomy in problem solving")
    print()
    
    while True:
        print("\n🎯 Demo Options:")
        print("1. Compare autonomous vs structured approaches")
        print("2. Watch autonomous problem solving in action")
        print("3. Compare all agent versions (V1 vs V2 vs V3)")
        print("4. Explore autonomous agent workspace")
        print("5. Exit")
        
        try:
            choice = input("\nChoose option (1-5): ").strip()
            
            if choice == "1":
                demonstrate_autonomous_behavior()
            elif choice == "2":
                demo_autonomous_problem_solving()
            elif choice == "3":
                compare_agent_versions()
            elif choice == "4":
                explore_workspace()
            elif choice == "5":
                print("👋 Thanks for exploring autonomous AI!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo ended by user")
            break

if __name__ == "__main__":
    main()
