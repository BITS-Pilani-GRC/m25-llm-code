"""
Fully Autonomous Coding Agent (Version 3)

This agent has complete autonomy in decision making:
- LLM decides which tool to use next
- No hardcoded workflow or sequence
- Dynamic, adaptive problem solving
- Self-determining stop conditions
- Creative and flexible approach

The agent operates purely based on LLM reasoning about what to do next.
"""

import os
import time
import json
from typing import Dict, Any, Optional
from datetime import datetime

from agent_state import AgentState, ToolCall
from tool_selector import AutonomousToolSelector
from tools import ThinkingTool, CodeGenerationTool, ReadFileTool, WriteFileTool, ExecutionTool

class FullyAutonomousCodingAgent:
    """
    Version 3: Fully Autonomous Coding Agent
    
    Key Features:
    - Complete LLM-driven decision making
    - No hardcoded workflows
    - Dynamic tool selection based on context
    - Self-regulated stopping conditions
    - Adaptive problem-solving strategies
    """
    
    def __init__(self, llm_client, workspace_path: str = "workspace", 
                 max_tool_calls: int = 15, verbose: bool = True):
        self.llm_client = llm_client
        self.workspace_path = workspace_path
        self.max_tool_calls = max_tool_calls
        self.verbose = verbose
        
        # Initialize tools
        self.tools = {
            "think": ThinkingTool(llm_client),
            "generate_code": CodeGenerationTool(llm_client),
            "read_file": ReadFileTool(workspace_path),
            "write_file": WriteFileTool(workspace_path),
            "execute_code": ExecutionTool(workspace_path)
        }
        
        # Initialize autonomous decision making
        self.tool_selector = AutonomousToolSelector(llm_client, self.tools)
        
        # Ensure workspace exists
        os.makedirs(workspace_path, exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "solutions"), exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "logs"), exist_ok=True)
        
        self.log(f"🤖 Fully Autonomous Agent initialized with {len(self.tools)} tools")
        self.log(f"📁 Workspace: {workspace_path}")
        self.log(f"🎯 Max tool calls: {max_tool_calls}")
    
    def solve_problem(self, problem_statement: str) -> Dict[str, Any]:
        """
        Autonomously solve a programming problem with complete freedom
        
        The agent will:
        1. Analyze the problem statement
        2. Dynamically decide which tools to use
        3. Adapt its approach based on results
        4. Stop when it determines the solution is satisfactory
        
        Args:
            problem_statement: The coding problem to solve
            
        Returns:
            Complete session results including all decisions and outcomes
        """
        self.log("🚀 Starting fully autonomous problem solving")
        self.log(f"📋 Problem: {problem_statement[:100]}...")
        
        # Initialize state tracking
        state = AgentState(problem_statement, self.max_tool_calls)
        session_start = time.time()
        
        try:
            # Main autonomous loop
            while state.remaining_calls > 0 and not state.is_satisfied:
                self.log(f"\n🔄 Tool Call {len(state.tool_calls) + 1}/{state.max_tool_calls}")
                
                # Let the LLM decide what to do next
                decision = self._make_autonomous_decision(state)
                
                if decision["action"] == "stop":
                    state.mark_satisfied(decision["reasoning"])
                    self.log(f"🛑 Agent decided to stop: {decision['reasoning']}")
                    break
                
                # Execute the chosen tool
                self._execute_tool_decision(decision, state)
                
                # Update agent's self-assessment
                self._update_agent_assessment(state)
            
            # Finalize the session
            session_time = time.time() - session_start
            final_report = self._generate_session_report(state, session_time)
            
            self.log(f"\n🎯 Session Complete!")
            self.log(f"📊 Result: {'SUCCESS' if state.is_satisfied else 'INCOMPLETE'}")
            self.log(f"⏱️ Time: {session_time:.1f}s")
            self.log(f"🔧 Tool calls: {len(state.tool_calls)}/{state.max_tool_calls}")
            
            return final_report
            
        except Exception as e:
            self.log(f"💥 Autonomous solving failed: {str(e)}")
            return self._generate_error_report(state, str(e))
    
    def _make_autonomous_decision(self, state: AgentState) -> Dict[str, Any]:
        """
        Use LLM to make the next decision autonomously
        
        This is the core of the autonomous behavior - the LLM analyzes
        the current state and decides what to do next.
        """
        self.log("🧠 Agent analyzing situation and making decision...")
        
        decision_start = time.time()
        decision = self.tool_selector.decide_next_action(state)
        decision_time = time.time() - decision_start
        
        if decision["action"] == "use_tool":
            tool_name = decision["tool"]
            reasoning = decision["reasoning"]
            self.log(f"🎯 Decision: Use {tool_name}")
            self.log(f"💭 Reasoning: {reasoning}")
            
            # Record the decision in state
            state.add_tool_call(tool_name, decision["parameters"], reasoning)
            
        else:  # stop decision
            self.log(f"🛑 Decision: Stop solving")
            self.log(f"💭 Reasoning: {decision['reasoning']}")
        
        self.log(f"⏱️ Decision time: {decision_time:.2f}s")
        return decision
    
    def _execute_tool_decision(self, decision: Dict[str, Any], state: AgentState) -> None:
        """Execute the tool that the agent decided to use"""
        tool_name = decision["tool"]
        parameters = decision["parameters"]
        
        self.log(f"🛠️ Executing {tool_name} with parameters: {parameters}")
        
        execution_start = time.time()
        
        try:
            # Execute the chosen tool
            tool_result = self.tools[tool_name].execute(**parameters)
            execution_time = time.time() - execution_start
            
            # Update state with the result
            state.update_last_tool_call(tool_result, execution_time)
            
            # Handle specific tool results
            self._process_tool_result(tool_name, tool_result, parameters, state)
            
            success_indicator = "✅" if tool_result.get("success", False) else "❌"
            self.log(f"{success_indicator} {tool_name} completed in {execution_time:.2f}s")
            
            if not tool_result.get("success", False):
                error = tool_result.get("error", "Unknown error")
                self.log(f"💥 Tool error: {error}")
                state.add_issue(f"{tool_name} failed: {error}")
            
        except Exception as e:
            execution_time = time.time() - execution_start
            error_result = {"success": False, "error": str(e)}
            state.update_last_tool_call(error_result, execution_time)
            
            self.log(f"💥 Tool execution failed: {str(e)}")
            state.add_issue(f"{tool_name} execution error: {str(e)}")
    
    def _process_tool_result(self, tool_name: str, result: Dict[str, Any], 
                           parameters: Dict[str, Any], state: AgentState) -> None:
        """Process specific tool results and update state accordingly"""
        
        if not result.get("success", False):
            return
        
        tool_result = result["result"]
        
        if tool_name == "think":
            # Record thinking process
            thinking_content = tool_result.get("thinking_process", "")
            state.add_thinking(f"Thinking: {thinking_content[:200]}...")
            
            # Update current approach if mentioned
            solution_plan = tool_result.get("solution_plan", "")
            if solution_plan:
                state.current_approach = solution_plan[:100] + "..." if len(solution_plan) > 100 else solution_plan
        
        elif tool_name == "generate_code":
            # Record code generation
            generated_code = tool_result.get("generated_code", "")
            state.add_thinking(f"Generated {len(generated_code)} characters of code")
        
        elif tool_name == "write_file":
            # Record file creation
            filename = parameters.get("filename", "unknown")
            content = parameters.get("content", "")
            content_type = parameters.get("type", "unknown")
            purpose = f"Tool call: {tool_name}"
            
            state.add_file(
                filename=filename,
                path=result["result"]["file_path"],
                content_type=content_type,
                purpose=purpose,
                size=len(content)
            )
            
            self.log(f"📄 Created file: {filename} ({len(content)} chars)")
        
        elif tool_name == "read_file":
            # Record file reading
            filename = parameters.get("filename", "unknown")
            content = tool_result.get("content", "")
            state.add_thinking(f"Read {filename}: {len(content)} characters")
        
        elif tool_name == "execute_code":
            # Record execution results
            filename = parameters.get("filename", "unknown")
            exit_code = tool_result.get("exit_code", -1)
            stdout = tool_result.get("stdout", "")
            stderr = tool_result.get("stderr", "")
            execution_time = tool_result.get("execution_time", 0)
            analysis = tool_result.get("analysis", {})
            
            state.add_execution_result(
                filename=filename,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                execution_time=execution_time,
                test_results=analysis.get("test_results", {})
            )
            
            # Log execution summary
            quality_score = analysis.get("test_results", {}).get("quality_score", 0)
            self.log(f"🚀 Executed {filename}: exit_code={exit_code}, quality={quality_score}/100")
    
    def _update_agent_assessment(self, state: AgentState) -> None:
        """Update the agent's self-assessment of progress and satisfaction"""
        
        # Calculate satisfaction based on progress
        satisfaction = 0
        confidence = 0
        
        # Base satisfaction from having files and executions
        if state.files_created:
            satisfaction += 20
        if state.execution_results:
            satisfaction += 20
        
        # Quality-based satisfaction
        if state.best_quality_score > 0:
            satisfaction += min(50, state.best_quality_score // 2)
        
        # Progress-based confidence
        if len(state.tool_calls) > 0:
            confidence += 20
        if state.best_quality_score >= 70:
            confidence += 50
        if not state.identified_issues:
            confidence += 30
        
        # Update state
        state.update_satisfaction(satisfaction)
        state.update_confidence(confidence)
        
        # Auto-satisfaction for very high quality
        if state.best_quality_score >= 90 and not state.is_satisfied:
            state.mark_satisfied(f"High quality solution achieved: {state.best_quality_score}/100")
    
    def _generate_session_report(self, state: AgentState, session_time: float) -> Dict[str, Any]:
        """Generate comprehensive session report"""
        
        # Calculate various metrics
        tool_usage_stats = self.tool_selector.get_tool_usage_stats(state)
        
        report = {
            "session_info": {
                "problem_statement": state.problem_statement,
                "session_duration": session_time,
                "total_tool_calls": len(state.tool_calls),
                "max_tool_calls": state.max_tool_calls,
                "completion_status": "SUCCESS" if state.is_satisfied else "INCOMPLETE"
            },
            "results": {
                "is_satisfied": state.is_satisfied,
                "stop_reason": state.stop_reason,
                "best_solution": state.best_solution,
                "best_quality_score": state.best_quality_score,
                "satisfaction_level": state.satisfaction_level,
                "confidence_level": state.confidence_level
            },
            "activity_summary": {
                "files_created": len(state.files_created),
                "code_executions": len(state.execution_results),
                "thinking_sessions": len(state.thinking_history),
                "issues_identified": len(state.identified_issues),
                "lessons_learned": len(state.lessons_learned)
            },
            "tool_usage": tool_usage_stats,
            "decision_trail": [
                {
                    "tool": call.tool_name,
                    "reasoning": call.reasoning,
                    "success": call.success,
                    "timestamp": call.timestamp
                }
                for call in state.tool_calls
            ],
            "workspace_artifacts": {
                "files": [
                    {
                        "filename": f.filename,
                        "type": f.content_type,
                        "purpose": f.purpose,
                        "size": f.size
                    }
                    for f in state.files_created
                ],
                "execution_logs": len(state.execution_results)
            },
            "state_data": state.to_dict()
        }
        
        # Save session report
        report_filename = f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(self.workspace_path, "logs", report_filename)
        
        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            self.log(f"📊 Session report saved: {report_filename}")
        except Exception as e:
            self.log(f"⚠️ Could not save session report: {e}")
        
        return report
    
    def _generate_error_report(self, state: AgentState, error: str) -> Dict[str, Any]:
        """Generate error report when session fails"""
        return {
            "session_info": {
                "problem_statement": state.problem_statement,
                "completion_status": "ERROR",
                "error": error
            },
            "results": {
                "is_satisfied": False,
                "stop_reason": f"Session error: {error}",
                "best_solution": state.best_solution,
                "best_quality_score": state.best_quality_score
            },
            "activity_summary": {
                "tool_calls_completed": len(state.tool_calls),
                "files_created": len(state.files_created),
                "executions_done": len(state.execution_results)
            },
            "state_data": state.to_dict()
        }
    
    def log(self, message: str) -> None:
        """Log a message if verbose mode is enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def get_capabilities_summary(self) -> str:
        """Get a summary of the agent's capabilities"""
        return f"""Fully Autonomous Coding Agent (V3) Capabilities:

🧠 AUTONOMOUS DECISION MAKING:
- LLM analyzes current state and decides next action
- No hardcoded workflows or sequences
- Dynamic adaptation to problem requirements
- Creative and flexible problem-solving approaches

🛠️ AVAILABLE TOOLS ({len(self.tools)}):
{chr(10).join(f'  - {name}: {tool.get_description()}' for name, tool in self.tools.items())}

🎯 INTELLIGENT FEATURES:
- Self-regulated stopping conditions
- Quality-based solution assessment
- Learning from previous attempts
- Comprehensive state tracking
- Session-wide context awareness

📊 AUTONOMOUS CAPABILITIES:
- Decides when to analyze problems
- Chooses coding approaches dynamically
- Determines testing strategies
- Self-evaluates solution quality
- Stops when satisfied with results

This agent represents true AI autonomy in coding problem solving."""
