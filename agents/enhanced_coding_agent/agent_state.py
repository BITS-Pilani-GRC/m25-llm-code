"""
Agent State Management for Fully Autonomous Coding Agent

This module provides comprehensive state tracking for the autonomous agent,
allowing it to make informed decisions based on its current context and history.
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ToolCall:
    """Represents a single tool call made by the agent"""
    tool_name: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]
    timestamp: str
    reasoning: str
    success: bool
    execution_time: float = 0.0

@dataclass
class ExecutionResult:
    """Detailed execution result from running code"""
    filename: str
    exit_code: int
    stdout: str
    stderr: str
    execution_time: float
    test_results: Dict[str, Any]
    quality_score: int = 0

@dataclass
class FileInfo:
    """Information about files in the workspace"""
    filename: str
    path: str
    content_type: str  # solution, test, analysis, helper, etc.
    created_at: str
    size: int
    purpose: str

class AgentState:
    """
    Comprehensive state tracking for the autonomous coding agent
    
    This class maintains all the context the agent needs to make
    intelligent decisions about what to do next.
    """
    
    def __init__(self, problem_statement: str, max_tool_calls: int = 15):
        # Core problem information
        self.problem_statement = problem_statement
        self.start_time = datetime.now().isoformat()
        
        # Tool call management
        self.max_tool_calls = max_tool_calls
        self.tool_calls: List[ToolCall] = []
        self.remaining_calls = max_tool_calls
        
        # Solution tracking
        self.files_created: List[FileInfo] = []
        self.execution_results: List[ExecutionResult] = []
        self.best_solution: Optional[str] = None
        self.best_quality_score = 0
        
        # Agent's mental state
        self.thinking_history: List[str] = []
        self.current_approach = ""
        self.identified_issues: List[str] = []
        self.attempted_solutions: List[str] = []
        
        # Progress tracking
        self.satisfaction_level = 0  # 0-100
        self.confidence_level = 0    # 0-100
        self.is_satisfied = False
        self.stop_reason = ""
        
        # Learning and adaptation
        self.failed_attempts: List[Dict[str, Any]] = []
        self.successful_patterns: List[str] = []
        self.lessons_learned: List[str] = []
    
    def add_tool_call(self, tool_name: str, parameters: Dict[str, Any], 
                     reasoning: str) -> None:
        """Record a new tool call attempt"""
        tool_call = ToolCall(
            tool_name=tool_name,
            parameters=parameters,
            result={},  # Will be filled when execution completes
            timestamp=datetime.now().isoformat(),
            reasoning=reasoning,
            success=False,  # Will be updated
        )
        self.tool_calls.append(tool_call)
        self.remaining_calls -= 1
    
    def update_last_tool_call(self, result: Dict[str, Any], 
                            execution_time: float = 0.0) -> None:
        """Update the result of the most recent tool call"""
        if self.tool_calls:
            last_call = self.tool_calls[-1]
            last_call.result = result
            last_call.success = result.get("success", False)
            last_call.execution_time = execution_time
    
    def add_file(self, filename: str, path: str, content_type: str, 
                purpose: str, size: int = 0) -> None:
        """Record a new file creation"""
        file_info = FileInfo(
            filename=filename,
            path=path,
            content_type=content_type,
            created_at=datetime.now().isoformat(),
            size=size,
            purpose=purpose
        )
        self.files_created.append(file_info)
    
    def add_execution_result(self, filename: str, exit_code: int, 
                           stdout: str, stderr: str, execution_time: float,
                           test_results: Dict[str, Any]) -> None:
        """Record code execution results"""
        # Calculate quality score based on execution
        quality_score = self._calculate_quality_score(
            exit_code, stdout, stderr, test_results
        )
        
        execution_result = ExecutionResult(
            filename=filename,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            execution_time=execution_time,
            test_results=test_results,
            quality_score=quality_score
        )
        
        self.execution_results.append(execution_result)
        
        # Update best solution if this is better
        if quality_score > self.best_quality_score:
            self.best_quality_score = quality_score
            self.best_solution = filename
    
    def add_thinking(self, thought: str) -> None:
        """Record agent's thinking process"""
        self.thinking_history.append(f"[{datetime.now().strftime('%H:%M:%S')}] {thought}")
    
    def add_issue(self, issue: str) -> None:
        """Record an identified issue"""
        if issue not in self.identified_issues:
            self.identified_issues.append(issue)
    
    def add_lesson(self, lesson: str) -> None:
        """Record a lesson learned"""
        if lesson not in self.lessons_learned:
            self.lessons_learned.append(lesson)
    
    def update_satisfaction(self, level: int, reason: str = "") -> None:
        """Update agent's satisfaction level"""
        self.satisfaction_level = max(0, min(100, level))
        if reason:
            self.add_thinking(f"Satisfaction updated to {level}/100: {reason}")
    
    def update_confidence(self, level: int, reason: str = "") -> None:
        """Update agent's confidence level"""
        self.confidence_level = max(0, min(100, level))
        if reason:
            self.add_thinking(f"Confidence updated to {level}/100: {reason}")
    
    def mark_satisfied(self, reason: str) -> None:
        """Mark the agent as satisfied with the solution"""
        self.is_satisfied = True
        self.stop_reason = reason
        self.add_thinking(f"SATISFIED: {reason}")
    
    def get_recent_actions(self, count: int = 3) -> List[str]:
        """Get the most recent tool call summaries"""
        recent = self.tool_calls[-count:] if len(self.tool_calls) >= count else self.tool_calls
        return [
            f"{call.tool_name}({', '.join(f'{k}={v}' if len(str(v)) < 30 else f'{k}=...' for k, v in call.parameters.items())}) → {'✅' if call.success else '❌'} {call.reasoning}"
            for call in recent
        ]
    
    def get_current_context_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of current state for LLM decision making"""
        return {
            "problem": self.problem_statement,
            "progress": {
                "tool_calls_used": len(self.tool_calls),
                "tool_calls_remaining": self.remaining_calls,
                "files_created": len(self.files_created),
                "executions_done": len(self.execution_results),
                "satisfaction_level": self.satisfaction_level,
                "confidence_level": self.confidence_level
            },
            "current_state": {
                "files_exist": [f.filename for f in self.files_created],
                "best_solution": self.best_solution,
                "best_quality_score": self.best_quality_score,
                "current_approach": self.current_approach,
                "identified_issues": self.identified_issues[-3:],  # Last 3 issues
                "recent_thoughts": self.thinking_history[-2:] if self.thinking_history else []
            },
            "recent_actions": self.get_recent_actions(3),
            "execution_summary": self._get_execution_summary(),
            "should_continue": not self.is_satisfied and self.remaining_calls > 0
        }
    
    def _calculate_quality_score(self, exit_code: int, stdout: str, 
                               stderr: str, test_results: Dict[str, Any]) -> int:
        """Calculate quality score for an execution (0-100)"""
        score = 0
        
        # Basic execution (30 points)
        if exit_code == 0:
            score += 30
        
        # Output presence (10 points)
        if stdout.strip():
            score += 10
        
        # Test results (50 points)
        if test_results.get("has_test_output", False):
            score += 10
            total_tests = test_results.get("total_tests", 0)
            passed_tests = test_results.get("passed_tests", 0)
            
            if total_tests > 0:
                pass_rate = passed_tests / total_tests
                score += int(40 * pass_rate)
        
        # No errors (10 points)
        if not stderr.strip():
            score += 10
        
        return min(100, score)
    
    def _get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all execution attempts"""
        if not self.execution_results:
            return {"executions": 0, "average_quality": 0, "best_quality": 0}
        
        qualities = [result.quality_score for result in self.execution_results]
        return {
            "executions": len(self.execution_results),
            "average_quality": sum(qualities) / len(qualities),
            "best_quality": max(qualities),
            "latest_quality": qualities[-1] if qualities else 0,
            "latest_exit_code": self.execution_results[-1].exit_code
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "problem_statement": self.problem_statement,
            "start_time": self.start_time,
            "tool_calls": [asdict(call) for call in self.tool_calls],
            "files_created": [asdict(file) for file in self.files_created],
            "execution_results": [asdict(result) for result in self.execution_results],
            "thinking_history": self.thinking_history,
            "satisfaction_level": self.satisfaction_level,
            "confidence_level": self.confidence_level,
            "is_satisfied": self.is_satisfied,
            "stop_reason": self.stop_reason,
            "best_solution": self.best_solution,
            "best_quality_score": self.best_quality_score
        }
    
    def save_to_file(self, filepath: str) -> None:
        """Save complete state to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def __str__(self) -> str:
        """Human-readable state summary"""
        return f"""AgentState Summary:
Problem: {self.problem_statement[:60]}...
Progress: {len(self.tool_calls)}/{self.max_tool_calls} tool calls
Files: {len(self.files_created)} created
Quality: {self.best_quality_score}/100 (best)
Satisfaction: {self.satisfaction_level}/100
Status: {'SATISFIED' if self.is_satisfied else 'WORKING'}"""
