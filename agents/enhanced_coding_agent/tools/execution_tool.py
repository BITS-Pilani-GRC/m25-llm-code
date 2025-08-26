"""
Execution Tool - Run Python scripts with comprehensive logging

This tool executes generated Python code and captures:
- Standard output and error streams
- Execution time and exit codes
- Detailed logging with timestamps
- Error analysis and reporting
"""

import os
import subprocess
import time
from datetime import datetime
from typing import Dict, Any
from .base_tool import BaseTool

class ExecutionTool(BaseTool):
    """
    Tool for executing Python scripts with comprehensive logging
    
    Features:
    - Execute Python files safely
    - Capture stdout, stderr, and exit codes
    - Generate timestamped log files
    - Measure execution time
    - Analyze execution results
    """
    
    def __init__(self, workspace_path: str = "workspace"):
        super().__init__("execute_code")
        self.workspace_path = workspace_path
        self.logs_dir = os.path.join(workspace_path, "logs")
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def execute(self, filename: str, directory: str = "solutions", 
                timeout: int = 30) -> Dict[str, Any]:
        """
        Execute a Python script and log the results
        
        Args:
            filename: Python file to execute
            directory: Subdirectory containing the file
            timeout: Maximum execution time in seconds
            
        Returns:
            Dict with execution results and log file info
        """
        try:
            # Construct file path
            if directory:
                script_path = os.path.join(self.workspace_path, directory, filename)
            else:
                script_path = os.path.join(self.workspace_path, filename)
            
            # Check if file exists
            if not os.path.exists(script_path):
                return self.format_result(
                    success=False,
                    error=f"Script not found: {script_path}"
                )
            
            # Generate timestamp for this execution
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            log_filename = f"execution_{timestamp}.log"
            log_path = os.path.join(self.logs_dir, log_filename)
            
            # Execute the Python script
            start_time = time.time()
            execution_result = self._run_python_script(script_path, timeout)
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Analyze the results
            analysis = self._analyze_execution_result(execution_result, execution_time)
            
            # Create detailed log entry
            log_content = self._create_log_content(
                script_path, execution_result, execution_time, analysis, timestamp
            )
            
            # Write log file
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            return self.format_result(
                success=True,
                result={
                    "stdout": execution_result["stdout"],
                    "stderr": execution_result["stderr"], 
                    "exit_code": execution_result["returncode"],
                    "execution_time": execution_time,
                    "log_file": log_path,
                    "log_filename": log_filename,
                    "analysis": analysis,
                    "timestamp": timestamp
                }
            )
            
        except Exception as e:
            return self.format_result(
                success=False,
                error=f"Execution tool error: {str(e)}"
            )
    
    def _run_python_script(self, script_path: str, timeout: int) -> Dict[str, Any]:
        """Run a Python script with timeout and capture output"""
        try:
            result = subprocess.run(
                ['python', script_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.dirname(script_path)
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "timed_out": False
            }
            
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {timeout} seconds",
                "returncode": -1,
                "timed_out": True
            }
        except FileNotFoundError:
            return {
                "stdout": "",
                "stderr": "Python interpreter not found",
                "returncode": -2,
                "timed_out": False
            }
    
    def _analyze_execution_result(self, result: Dict[str, Any], execution_time: float) -> Dict[str, Any]:
        """Analyze execution results to determine success/failure patterns"""
        analysis = {
            "success": result["returncode"] == 0 and not result["timed_out"],
            "has_output": bool(result["stdout"].strip()),
            "has_errors": bool(result["stderr"].strip()),
            "timed_out": result["timed_out"],
            "execution_time_category": self._categorize_execution_time(execution_time),
            "test_results": self._parse_test_results(result["stdout"]),
            "error_analysis": self._analyze_errors(result["stderr"]) if result["stderr"] else None
        }
        
        return analysis
    
    def _categorize_execution_time(self, execution_time: float) -> str:
        """Categorize execution time"""
        if execution_time < 0.1:
            return "very_fast"
        elif execution_time < 1.0:
            return "fast"
        elif execution_time < 5.0:
            return "normal"
        elif execution_time < 15.0:
            return "slow"
        else:
            return "very_slow"
    
    def _parse_test_results(self, stdout: str) -> Dict[str, Any]:
        """Parse test results from stdout to determine pass/fail status"""
        test_info = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "has_test_output": False
        }
        
        lines = stdout.split('\n')
        for line in lines:
            line_lower = line.lower()
            if '✅' in line or 'passed' in line_lower:
                test_info["passed_tests"] += 1
                test_info["has_test_output"] = True
            elif '❌' in line or 'failed' in line_lower:
                test_info["failed_tests"] += 1
                test_info["has_test_output"] = True
            elif 'test case' in line_lower or 'testing' in line_lower:
                test_info["has_test_output"] = True
        
        test_info["total_tests"] = test_info["passed_tests"] + test_info["failed_tests"]
        return test_info
    
    def _analyze_errors(self, stderr: str) -> Dict[str, Any]:
        """Analyze error messages to categorize the type of errors"""
        error_analysis = {
            "error_type": "unknown",
            "is_syntax_error": False,
            "is_runtime_error": False,
            "is_import_error": False,
            "error_summary": stderr.split('\n')[-2] if stderr.strip() else ""
        }
        
        stderr_lower = stderr.lower()
        
        if "syntaxerror" in stderr_lower:
            error_analysis["error_type"] = "syntax"
            error_analysis["is_syntax_error"] = True
        elif "importerror" in stderr_lower or "modulenotfounderror" in stderr_lower:
            error_analysis["error_type"] = "import"
            error_analysis["is_import_error"] = True
        elif any(err in stderr_lower for err in ["nameerror", "typeerror", "valueerror", "attributeerror"]):
            error_analysis["error_type"] = "runtime"
            error_analysis["is_runtime_error"] = True
        
        return error_analysis
    
    def _create_log_content(self, script_path: str, result: Dict[str, Any], 
                          execution_time: float, analysis: Dict[str, Any], timestamp: str) -> str:
        """Create detailed log content for the execution"""
        log_content = f"""EXECUTION LOG - {timestamp}
{'='*60}

SCRIPT: {script_path}
EXECUTION TIME: {execution_time:.3f} seconds
EXIT CODE: {result['returncode']}
STATUS: {'SUCCESS' if analysis['success'] else 'FAILED'}

ANALYSIS:
- Has Output: {analysis['has_output']}
- Has Errors: {analysis['has_errors']}
- Timed Out: {analysis['timed_out']}
- Performance: {analysis['execution_time_category']}

TEST RESULTS:
- Total Tests: {analysis['test_results']['total_tests']}
- Passed: {analysis['test_results']['passed_tests']}
- Failed: {analysis['test_results']['failed_tests']}
- Has Test Output: {analysis['test_results']['has_test_output']}

STANDARD OUTPUT:
{'-'*40}
{result['stdout']}

STANDARD ERROR:
{'-'*40}
{result['stderr']}

"""
        
        if analysis['error_analysis']:
            log_content += f"""ERROR ANALYSIS:
- Error Type: {analysis['error_analysis']['error_type']}
- Syntax Error: {analysis['error_analysis']['is_syntax_error']}
- Runtime Error: {analysis['error_analysis']['is_runtime_error']}
- Import Error: {analysis['error_analysis']['is_import_error']}
- Summary: {analysis['error_analysis']['error_summary']}

"""
        
        log_content += f"{'='*60}\nEND OF LOG"
        
        return log_content
    
    def get_description(self) -> str:
        return "Execute Python scripts and generate comprehensive execution logs with analysis"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_code",
                "description": self.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Python file to execute"
                        },
                        "directory": {
                            "type": "string",
                            "description": "Subdirectory containing the file (default: 'solutions')"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Maximum execution time in seconds (default: 30)"
                        }
                    },
                    "required": ["filename"]
                }
            }
        }
