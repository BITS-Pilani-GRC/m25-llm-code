# Coding Agents Demo

Educational demonstration of LLM-powered coding agents for understanding how AI can read, analyze, and modify code.

## Overview

This demo shows the progression from simple code analysis to automated bug fixing, demonstrating key concepts of coding agents:

- **Tool Usage**: How agents use functions to interact with the environment
- **Code Understanding**: How LLMs can read and analyze code
- **Environment Interaction**: Reading files, writing files, executing code
- **Iterative Problem Solving**: Read → Analyze → Fix → Verify cycles

## Structure

```
agents/
├── base_agent.py          # Foundation class for all agents
├── v1_code_reader.py      # Version 1: Code analysis agent
├── v2_code_fixer.py       # Version 2: Bug fixing agent
├── demo.py               # Main demonstration script
├── examples/             # Sample code files for testing
│   ├── simple_function.py    # Clean code for analysis
│   ├── buggy_math.py         # Code with obvious bugs
│   └── string_processor.py   # More complex examples
└── README.md             # This file
```

## Quick Start

1. **Run the full demo:**
   ```bash
   cd agents
   python demo.py
   ```

2. **Test individual agents:**
   ```bash
   python v1_code_reader.py
   python v2_code_fixer.py
   ```

## Version Progression

### Version 1: Code Reader Agent
- **Purpose**: Demonstrate LLM code understanding
- **Capabilities**: 
  - Read source files
  - Explain what code does
  - Predict outputs for given inputs
  - Identify patterns and structure
- **Tools**: `read_file`
- **Learning Focus**: Basic LLM-tool integration

### Version 2: Code Fixer Agent  
- **Purpose**: Show automated bug fixing
- **Capabilities**:
  - All of Version 1, plus:
  - Identify bugs and issues
  - Generate fixed code
  - Execute and verify fixes
- **Tools**: `read_file`, `write_file`, `execute_python`
- **Learning Focus**: Observation-action loops, iteration

## Using with Real LLMs

The demo works with either real LLM APIs or a mock client:

### With Gemini API:
1. Install dependencies: `pip install google-genai python-dotenv`
2. Set your API key: `export GEMINI_API_KEY="your-key-here"`
3. Run the demo - it will automatically use Gemini

### With Mock Client:
- No setup needed
- Shows agent structure and flow
- Uses pre-programmed responses for common scenarios

## Example Usage

### Analyzing Code:
```python
from v1_code_reader import CodeReaderAgent

agent = CodeReaderAgent(llm_client)
analysis = agent.analyze_code("examples/simple_function.py", 
                            "What does mystery_function do?")
print(analysis)
```

### Fixing Bugs:
```python
from v2_code_fixer import CodeFixerAgent

agent = CodeFixerAgent(llm_client)
report = agent.fix_code("examples/buggy_math.py",
                       "Circle area should be πr²")
print(report)
```

## Key Educational Points

1. **Tool Design**: How to create simple, focused tools
2. **LLM Integration**: Using prompts to guide agent behavior  
3. **Error Handling**: Graceful handling of file and execution errors
4. **Iterative Processes**: How agents can improve through feedback
5. **Environment Interaction**: File system operations for code manipulation

## Extension Ideas

Students can extend these agents by:

- Adding new tools (git operations, linting, testing)
- Implementing more sophisticated error recovery
- Adding support for multiple programming languages
- Creating specialized agents for specific domains
- Building agent collaboration workflows

## Dependencies

- Python 3.7+
- No external packages required for basic functionality
- Optional: OpenAI API key for real LLM integration

## Notes for Instructors

- Each agent is self-contained with simple testing functions
- Mock LLM responses help students understand the flow even without API access
- Examples progress from trivial to moderately complex
- Code is heavily commented for educational clarity
- Error handling demonstrates real-world considerations
