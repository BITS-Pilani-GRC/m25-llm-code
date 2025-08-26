"""
Enhanced Autonomous Coding Agent

This agent can autonomously solve programming problems by:
1. Thinking through the problem
2. Generating code solutions 
3. Executing and testing the code
4. Iterating based on results
5. Making all tool decisions via LLM reasoning

The agent operates in a loop until it achieves a satisfactory solution.
"""

import os
import json
from typing import Dict, Any, List, Optional
from tools import ThinkingTool, CodeGenerationTool, ReadFileTool, WriteFileTool, ExecutionTool

class EnhancedCodingAgent:
    """
    Autonomous coding agent that solves problems iteratively
    
    Features:
    - LLM-driven tool selection and decision making
    - Iterative problem solving with self-correction
    - Comprehensive logging and analysis
    - Autonomous workflow management
    """
    
    def __init__(self, llm_client, workspace_path: str = "workspace", max_iterations: int = 5):
        self.llm_client = llm_client
        self.workspace_path = workspace_path
        self.max_iterations = max_iterations
        
        # Initialize all tools
        self.tools = {
            "think": ThinkingTool(llm_client),
            "generate_code": CodeGenerationTool(llm_client),
            "read_file": ReadFileTool(workspace_path),
            "write_file": WriteFileTool(workspace_path),
            "execute_code": ExecutionTool(workspace_path)
        }
        
        # Track the agent's state throughout the session
        self.session_state = {
            "problem_statement": "",
            "current_iteration": 0,
            "attempts": [],
            "best_solution": None,
            "success_achieved": False
        }
        
        # Ensure workspace exists
        os.makedirs(workspace_path, exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "solutions"), exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "logs"), exist_ok=True)
    
    def solve_problem(self, problem_statement: str) -> Dict[str, Any]:
        """
        Autonomously solve a programming problem
        
        Args:
            problem_statement: The coding problem to solve
            
        Returns:
            Dict with solution results, attempts, and final status
        """
        print(f"🤖 Enhanced Coding Agent starting problem solving...")
        print(f"📋 Problem: {problem_statement[:100]}...")
        
        self.session_state["problem_statement"] = problem_statement
        self.session_state["current_iteration"] = 0
        self.session_state["attempts"] = []
        
        # Main solving loop
        while self.session_state["current_iteration"] < self.max_iterations:
            iteration = self.session_state["current_iteration"] + 1
            print(f"\n🔄 Iteration {iteration}/{self.max_iterations}")
            
            try:
                # Execute one iteration of the solving process
                iteration_result = self._execute_iteration()
                
                # Record this attempt
                self.session_state["attempts"].append(iteration_result)
                self.session_state["current_iteration"] = iteration
                
                # Check if we achieved success
                if iteration_result.get("success", False):
                    self.session_state["success_achieved"] = True
                    self.session_state["best_solution"] = iteration_result
                    print(f"✅ Problem solved successfully in iteration {iteration}!")
                    break
                else:
                    print(f"❌ Iteration {iteration} failed. Analyzing and trying again...")
                    
            except Exception as e:
                error_result = {
                    "iteration": iteration,
                    "success": False,
                    "error": f"Iteration failed with exception: {str(e)}",
                    "timestamp": self._get_timestamp()
                }
                self.session_state["attempts"].append(error_result)
                print(f"💥 Iteration {iteration} failed with error: {str(e)}")
        
        # Generate final report
        final_report = self._generate_final_report()
        print(f"\n📊 Final Result: {'SUCCESS' if self.session_state['success_achieved'] else 'FAILED'}")
        
        return final_report
    
    def _execute_iteration(self) -> Dict[str, Any]:
        """
        Execute one complete iteration of the solving process
        
        Returns:
            Dict with iteration results
        """
        iteration = self.session_state["current_iteration"] + 1
        iteration_start_time = self._get_timestamp()
        
        print(f"  🧠 Step 1: Thinking and planning...")
        
        # Step 1: Think about the problem
        thinking_result = self._execute_thinking_step()
        if not thinking_result["success"]:
            return self._format_iteration_result(iteration, False, "thinking_failed", 
                                               error=thinking_result.get("error"))
        
        print(f"  💻 Step 2: Generating code...")
        
        # Step 2: Generate code based on thinking
        code_result = self._execute_code_generation_step(thinking_result["result"])
        if not code_result["success"]:
            return self._format_iteration_result(iteration, False, "code_generation_failed",
                                               error=code_result.get("error"))
        
        print(f"  💾 Step 3: Saving solution...")
        
        # Step 3: Save the generated code
        save_result = self._execute_save_step(code_result["result"], iteration)
        if not save_result["success"]:
            return self._format_iteration_result(iteration, False, "save_failed",
                                               error=save_result.get("error"))
        
        print(f"  🚀 Step 4: Executing and testing...")
        
        # Step 4: Execute the code
        execution_result = self._execute_execution_step(save_result["filename"])
        if not execution_result["success"]:
            return self._format_iteration_result(iteration, False, "execution_failed",
                                               error=execution_result.get("error"))
        
        print(f"  📋 Step 5: Evaluating results...")
        
        # Step 5: Evaluate if the solution is satisfactory
        evaluation = self._evaluate_solution(execution_result["result"])
        
        return self._format_iteration_result(
            iteration, 
            evaluation["satisfactory"],
            "completed",
            thinking=thinking_result["result"],
            code=code_result["result"],
            execution=execution_result["result"],
            evaluation=evaluation,
            filename=save_result["filename"]
        )
    
    def _execute_thinking_step(self) -> Dict[str, Any]:
        """Execute the thinking tool"""
        previous_attempts = [
            attempt.get("error", "Unknown error") 
            for attempt in self.session_state["attempts"] 
            if not attempt.get("success", False)
        ]
        
        return self.tools["think"].execute(
            problem_statement=self.session_state["problem_statement"],
            previous_attempts=previous_attempts if previous_attempts else None
        )
    
    def _execute_code_generation_step(self, thinking_output: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the code generation tool"""
        # Get previous code if available
        previous_code = None
        execution_feedback = None
        
        if self.session_state["attempts"]:
            last_attempt = self.session_state["attempts"][-1]
            if "code" in last_attempt:
                previous_code = last_attempt["code"].get("generated_code")
            if "execution" in last_attempt:
                execution_feedback = self._format_execution_feedback(last_attempt["execution"])
        
        return self.tools["generate_code"].execute(
            problem_statement=self.session_state["problem_statement"],
            thinking_output=thinking_output["thinking_process"],
            previous_code=previous_code,
            execution_feedback=execution_feedback
        )
    
    def _execute_save_step(self, code_result: Dict[str, Any], iteration: int) -> Dict[str, Any]:
        """Save the generated code to a file"""
        filename = f"solution_v{iteration}.py"
        
        result = self.tools["write_file"].execute(
            filename=filename,
            content=code_result["generated_code"],
            directory="solutions"
        )
        
        if result["success"]:
            result["filename"] = filename
        
        return result
    
    def _execute_execution_step(self, filename: str) -> Dict[str, Any]:
        """Execute the saved code file"""
        return self.tools["execute_code"].execute(
            filename=filename,
            directory="solutions"
        )
    
    def _evaluate_solution(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate if the solution is satisfactory
        
        A solution is considered satisfactory if:
        - It executes without errors
        - It produces test output
        - Most/all tests pass
        """
        evaluation = {
            "satisfactory": False,
            "score": 0,
            "reasons": [],
            "issues": []
        }
        
        # Check basic execution success
        if execution_result["exit_code"] == 0:
            evaluation["score"] += 30
            evaluation["reasons"].append("Code executed without errors")
        else:
            evaluation["issues"].append(f"Exit code: {execution_result['exit_code']}")
        
        # Check for test output
        analysis = execution_result.get("analysis", {})
        test_results = analysis.get("test_results", {})
        
        if test_results.get("has_test_output", False):
            evaluation["score"] += 20
            evaluation["reasons"].append("Code produced test output")
            
            # Check test success rate
            total_tests = test_results.get("total_tests", 0)
            passed_tests = test_results.get("passed_tests", 0)
            
            if total_tests > 0:
                success_rate = passed_tests / total_tests
                if success_rate >= 0.8:  # 80% or more tests pass
                    evaluation["score"] += 40
                    evaluation["reasons"].append(f"High test success rate: {passed_tests}/{total_tests}")
                elif success_rate >= 0.5:  # 50% or more tests pass
                    evaluation["score"] += 20
                    evaluation["reasons"].append(f"Moderate test success rate: {passed_tests}/{total_tests}")
                else:
                    evaluation["issues"].append(f"Low test success rate: {passed_tests}/{total_tests}")
            else:
                evaluation["issues"].append("No test cases detected")
        else:
            evaluation["issues"].append("No test output detected")
        
        # Check for output presence
        if analysis.get("has_output", False):
            evaluation["score"] += 10
            evaluation["reasons"].append("Code produced output")
        
        # Determine if satisfactory (score >= 70)
        evaluation["satisfactory"] = evaluation["score"] >= 70
        
        return evaluation
    
    def _format_execution_feedback(self, execution_result: Dict[str, Any]) -> str:
        """Format execution results as feedback for the next iteration"""
        feedback = []
        
        if execution_result["exit_code"] != 0:
            feedback.append(f"Execution failed with exit code {execution_result['exit_code']}")
        
        if execution_result["stderr"]:
            feedback.append(f"Errors: {execution_result['stderr']}")
        
        analysis = execution_result.get("analysis", {})
        if not analysis.get("test_results", {}).get("has_test_output", False):
            feedback.append("No test output detected - ensure tests are running")
        
        test_results = analysis.get("test_results", {})
        if test_results.get("failed_tests", 0) > 0:
            feedback.append(f"Some tests failed: {test_results['failed_tests']} failed, {test_results['passed_tests']} passed")
        
        return " | ".join(feedback)
    
    def _format_iteration_result(self, iteration: int, success: bool, status: str, **kwargs) -> Dict[str, Any]:
        """Format the results of an iteration"""
        result = {
            "iteration": iteration,
            "success": success,
            "status": status,
            "timestamp": self._get_timestamp()
        }
        result.update(kwargs)
        return result
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate a comprehensive final report"""
        return {
            "problem_statement": self.session_state["problem_statement"],
            "success": self.session_state["success_achieved"],
            "total_iterations": self.session_state["current_iteration"],
            "max_iterations": self.max_iterations,
            "attempts": self.session_state["attempts"],
            "best_solution": self.session_state["best_solution"],
            "workspace_path": self.workspace_path,
            "summary": self._generate_summary()
        }
    
    def _generate_summary(self) -> str:
        """Generate a human-readable summary"""
        if self.session_state["success_achieved"]:
            return f"✅ Successfully solved the problem in {self.session_state['current_iteration']} iterations."
        else:
            return f"❌ Failed to solve the problem after {self.session_state['current_iteration']} iterations."
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_tools_description(self) -> str:
        """Get descriptions of all available tools"""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.get_description()}")
        return "\n".join(descriptions)
