# Enhanced Coding Agents Collection

A progressive collection of AI coding agents demonstrating different levels of autonomy and sophistication:

- **V2 Enhanced Agent**: Structured autonomous agent with predefined workflows
- **V3 Fully Autonomous Agent**: Complete LLM-driven decision making with dynamic workflows

## Overview

This collection showcases the evolution of AI coding agents from structured to fully autonomous:

### V2 Enhanced Agent (Structured Autonomy)
- **🔄 Iterative Problem Solving**: Learns from failures and improves solutions  
- **🛠️ Tool-Based Architecture**: Modular tools for different capabilities
- **📊 Comprehensive Logging**: Detailed execution tracking and analysis
- **🎯 Self-Evaluation**: Automatically determines solution quality
- **⚙️ Structured Workflow**: Predefined sequence of operations

### V3 Fully Autonomous Agent (Complete Autonomy)
- **🧠 LLM-Driven Decisions**: Every tool choice made by AI reasoning
- **🔄 Dynamic Workflows**: No hardcoded sequences or patterns
- **🎯 Context-Aware Actions**: Decisions based on current state analysis
- **🛑 Self-Regulated Stopping**: Agent determines when solution is satisfactory
- **🚀 Creative Problem-Solving**: Adaptive approaches to different problems

## Architecture

```
enhanced_coding_agent/
├── agent.py                    # V2: Structured autonomous agent
├── v3_autonomous_agent.py      # V3: Fully autonomous agent
├── agent_state.py              # V3: Rich state management system
├── tool_selector.py            # V3: LLM-driven tool selection
├── tools/                      # Shared tool implementations
│   ├── thinking_tool.py        # LLM-based problem analysis
│   ├── code_gen_tool.py        # LLM-based code generation
│   ├── file_tools.py           # Read/write file operations
│   ├── execution_tool.py       # Code execution with logging
│   └── base_tool.py           # Base tool interface
├── workspace/                  # V2 Agent working directory
├── workspace_v3/               # V3 Agent working directory
│   ├── solutions/             # Generated code solutions
│   └── logs/                  # Execution logs + session reports
├── examples/                   # Test problems
│   └── simple_problems.py     # Predefined coding problems
├── demo.py                    # V2 Interactive demonstration
├── v3_demo.py                 # V3 Autonomous agent demo
└── README.md                  # This file
```

## Key Features

### 🤖 V2 Structured Workflow (Predictable)

The V2 agent follows this structured autonomous loop:

1. **🧠 THINK**: Analyze problem, plan approach, learn from failures
2. **💻 GENERATE**: Create complete Python solution with tests
3. **💾 SAVE**: Write solution to file with proper naming
4. **🚀 EXECUTE**: Run code and capture comprehensive results
5. **📋 EVALUATE**: Determine if solution meets quality criteria
6. **🔄 ITERATE**: Repeat until success or max iterations reached

### 🧠 V3 Fully Autonomous Workflow (Dynamic)

The V3 agent has **NO predefined workflow**. Instead:

**🎯 LLM Decides Everything:**
- Which tool to use next based on current context
- When to think, code, test, or stop
- How many times to use each tool
- What parameters to pass to tools
- When the solution is satisfactory

**🔄 Example Dynamic Flows:**
```
Flow A: think → think → generate_code → write_file → execute_code → STOP
Flow B: think → generate_code → write_file → execute_code → read_file → think → generate_code → STOP  
Flow C: think → generate_code → write_file → execute_code → execute_code → think → STOP
```

Each problem gets a **unique, adaptive workflow** based on the agent's reasoning!

### 🛠️ Five Specialized Tools

#### 1. Thinking Tool (`think`)
- **Purpose**: Problem analysis and planning
- **LLM Usage**: Strategic reasoning and pseudocode generation
- **Features**: Learns from previous failed attempts

#### 2. Code Generation Tool (`generate_code`)
- **Purpose**: Complete solution generation
- **LLM Usage**: Python code creation with comprehensive tests
- **Features**: Self-contained scripts with clear test reporting

#### 3. Write File Tool (`write_file`)
- **Purpose**: Save generated content
- **Features**: Directory creation, overwrite protection, metadata tracking

#### 4. Read File Tool (`read_file`)
- **Purpose**: Access saved content
- **Features**: Error handling, file metadata, encoding support

#### 5. Execution Tool (`execute_code`)
- **Purpose**: Run and analyze Python scripts
- **Features**: Timestamped logging, performance analysis, error categorization

### 📊 Intelligent Evaluation

Solutions are automatically evaluated based on:
- ✅ **Execution Success**: No runtime errors
- ✅ **Test Coverage**: Presence of comprehensive tests
- ✅ **Test Results**: High pass rate (80%+ for success)
- ✅ **Output Quality**: Meaningful program output

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install google-genai python-dotenv

# Set up Gemini API key
export GEMINI_API_KEY="your-gemini-api-key"
```

### 2. Run Demos

```bash
cd enhanced_coding_agent

# V2 Structured Agent Demo
python demo.py

# V3 Fully Autonomous Agent Demo  
python v3_demo.py
```

### 3. Example Usage

#### V2 Structured Agent
```python
from agent import EnhancedCodingAgent
from demo import GeminiLLMClient

# Initialize structured agent
llm_client = GeminiLLMClient()
agent = EnhancedCodingAgent(llm_client, max_iterations=5)

# Solve with predefined workflow
result = agent.solve_problem("Write a two sum function...")
print(f"Success: {result['success']}")
```

#### V3 Fully Autonomous Agent
```python
from v3_autonomous_agent import FullyAutonomousCodingAgent
from v3_demo import GeminiLLMClient

# Initialize fully autonomous agent
llm_client = GeminiLLMClient()
agent = FullyAutonomousCodingAgent(llm_client, max_tool_calls=15)

# Solve with complete autonomy
result = agent.solve_problem("Write a two sum function...")
print(f"Autonomous result: {result['session_info']['completion_status']}")
print(f"Agent decision trail: {len(result['decision_trail'])} autonomous decisions")
```

## Demo Modes

### 1. Automated Demo
- Choose from predefined problems
- Watch agent solve step-by-step
- See generated solutions and test results

### 2. Interactive Mode
- Enter your own programming problems
- Real-time autonomous solving
- Custom problem exploration

### 3. Workspace Explorer
- Browse generated solutions
- Examine execution logs
- Analyze agent decision process

## Example Problems Included

1. **Two Sum** (Easy): Find indices of numbers that sum to target
2. **Palindrome Check** (Easy): Detect palindromic strings
3. **Fibonacci** (Easy): Generate nth Fibonacci number
4. **Word Count** (Medium): Count word frequencies in text
5. **List Rotation** (Medium): Rotate array elements

## Generated Solution Structure

Each solution is a self-contained Python script:

```python
def solution_function(params):
    """Main solution implementation"""
    # Agent-generated code here
    pass

def run_tests():
    """Comprehensive test suite"""
    test_cases = [
        {"input": ..., "expected": ..., "description": "..."},
        # Multiple test cases including edge cases
    ]
    
    # Detailed test execution with clear reporting
    # Shows: Input, Expected, Actual, Pass/Fail status
    
if __name__ == "__main__":
    run_tests()
```

## Logging and Analysis

### Execution Logs
Each run generates timestamped logs in `workspace/logs/`:

```
execution_20241201_143022.log
execution_20241201_143055.log
```

### Log Content
- Script path and execution time
- Exit codes and error analysis
- Test results and performance metrics
- Standard output and error streams
- Categorized error types (syntax, runtime, import)

## Educational Value

This enhanced agent teaches:

1. **🤖 Autonomous AI Systems**: How LLMs can make complex decisions
2. **🔧 Tool-Based Architecture**: Building modular AI capabilities
3. **🔄 Iterative Problem Solving**: Self-improvement through feedback
4. **📊 Solution Evaluation**: Automated quality assessment
5. **🛠️ Production AI Patterns**: Real-world AI system design

## Extending the Agent

### Add New Tools
```python
from tools.base_tool import BaseTool

class MyCustomTool(BaseTool):
    def execute(self, **kwargs):
        # Tool implementation
        pass
    
    def get_description(self):
        return "Description for LLM"
    
    def get_schema(self):
        return {"type": "function", ...}
```

### Customize Evaluation Criteria
Modify `_evaluate_solution()` in `agent.py` to change success criteria.

### Add Problem Types
Extend `examples/simple_problems.py` with new problem categories.

## Agent Evolution Comparison

| Feature | V1 (Reader) | V2 (Enhanced) | **V3 (Autonomous)** |
|---------|-------------|---------------|---------------------|
| **Autonomy Level** | 10% | 60% | **95%** |
| **Decision Making** | Human | Structured | **Fully LLM-driven** |
| **Workflow** | Manual | Hardcoded Loop | **Dynamic & Adaptive** |
| **Tool Selection** | Predetermined | Sequential | **Context-aware** |
| **Iteration Style** | None | Fixed Pattern | **Creative & Flexible** |
| **Stopping Logic** | Manual | Rule-based | **Self-determined** |
| **Learning** | None | Basic | **Adaptive** |
| **Creativity** | Low | Medium | **High** |
| **Real-world Similarity** | Low | Medium | **Excellent** |

### Key Differences: V2 vs V3

#### V2 Enhanced Agent (Structured)
```python
# Predictable workflow
while iteration < max_iterations:
    think() → generate_code() → write_file() → execute_code() → evaluate()
    if satisfied: break
```
- ✅ Reliable and consistent
- ✅ Easy to understand and debug  
- ❌ Inflexible workflow
- ❌ Can't adapt to different problem types

#### V3 Autonomous Agent (Dynamic)
```python
# Completely flexible workflow
while tool_calls < max_calls and not agent_satisfied:
    decision = llm.decide_what_to_do_next(current_state)
    if decision == "STOP": break
    execute_tool(decision.tool, decision.params)
```
- ✅ **Maximum flexibility and creativity**
- ✅ **Adapts to any problem type**
- ✅ **True AI autonomy demonstration**
- ✅ **Realistic AI agent behavior**
- ⚠️ Less predictable (requires robust LLM)

## Requirements

- Python 3.7+
- `google-genai` (for Gemini API)
- `python-dotenv` (for environment variables)
- Gemini API key (or works with mock client)

## Notes for Instructors

- **Progressive Complexity**: Start with basic problems, advance to complex ones
- **Observable Decision Making**: All LLM decisions are logged and visible
- **Failure Analysis**: Failed attempts provide learning opportunities
- **Modular Design**: Easy to modify and extend for different use cases
- **Real-world Patterns**: Demonstrates production AI system architecture

The enhanced agent showcases how AI can autonomously solve complex problems through structured reasoning, iterative improvement, and comprehensive self-evaluation.
