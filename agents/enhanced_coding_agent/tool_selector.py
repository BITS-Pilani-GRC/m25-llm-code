"""
Dynamic Tool Selection Engine for Fully Autonomous Coding Agent

This module implements LLM-driven tool selection where the agent decides
which tool to use next based on current context and state.
"""

import json
from typing import Dict, Any, Optional, List
from agent_state import AgentState

class AutonomousToolSelector:
    """
    LLM-driven tool selection engine
    
    This class uses the LLM to analyze the current state and decide
    which tool should be called next, including parameters and reasoning.
    """
    
    def __init__(self, llm_client, available_tools: Dict[str, Any]):
        self.llm_client = llm_client
        self.available_tools = available_tools
        self.tool_schemas = self._build_tool_schemas()
    
    def decide_next_action(self, state: AgentState) -> Dict[str, Any]:
        """
        Use LLM to decide the next tool call based on current state
        
        Args:
            state: Current agent state with full context
            
        Returns:
            Dict with tool name, parameters, and reasoning, or STOP decision
        """
        context = state.get_current_context_summary()
        
        # Build the decision prompt
        decision_prompt = self._build_decision_prompt(context, state)
        
        # Get LLM decision
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": decision_prompt}
        ]
        
        llm_response = self.llm_client.complete(messages)
        
        # Parse the LLM response
        decision = self._parse_llm_decision(llm_response, state)
        
        return decision
    
    def _get_system_prompt(self) -> str:
        """System prompt that defines the autonomous agent's role"""
        return """You are a fully autonomous coding agent with complete decision-making authority.

YOUR ROLE:
- Analyze the current state and decide what to do next
- Choose which tool to use based on context and needs
- Determine when you're satisfied with the solution
- Think strategically about the best approach

DECISION PROCESS:
1. Understand the current situation
2. Identify what needs to be done next
3. Choose the most appropriate tool
4. Provide clear reasoning for your choice
5. Decide if you should stop (satisfied) or continue

RESPONSE FORMAT:
You must respond with a valid JSON object in one of these formats:

For tool calls:
{
    "action": "use_tool",
    "tool": "tool_name",
    "parameters": {
        "param1": "value1",
        "param2": "value2"
    },
    "reasoning": "Clear explanation of why you chose this tool and these parameters"
}

For stopping:
{
    "action": "stop",
    "reasoning": "Clear explanation of why you're satisfied with the current solution"
}

IMPORTANT:
- Be strategic and thoughtful in your decisions
- Don't repeat the same action if it didn't work
- Learn from previous attempts
- Focus on solving the problem effectively
- Only stop when you're truly satisfied with the solution quality"""
    
    def _build_decision_prompt(self, context: Dict[str, Any], state: AgentState) -> str:
        """Build the complete decision prompt with all context"""
        
        prompt = f"""AUTONOMOUS DECISION REQUIRED

PROBLEM TO SOLVE:
{context['problem']}

CURRENT PROGRESS:
- Tool calls used: {context['progress']['tool_calls_used']}/{state.max_tool_calls}
- Tool calls remaining: {context['progress']['tool_calls_remaining']}
- Files created: {context['progress']['files_created']}
- Code executions: {context['progress']['executions_done']}
- Current satisfaction: {context['progress']['satisfaction_level']}/100
- Current confidence: {context['progress']['confidence_level']}/100

CURRENT STATE:
- Files in workspace: {context['current_state']['files_exist']}
- Best solution so far: {context['current_state']['best_solution']}
- Best quality score: {context['current_state']['best_quality_score']}/100
- Current approach: {context['current_state']['current_approach']}
- Recent issues identified: {context['current_state']['identified_issues']}

RECENT ACTIONS:
{chr(10).join(context['recent_actions']) if context['recent_actions'] else 'No previous actions'}

EXECUTION SUMMARY:
{self._format_execution_summary(context['execution_summary'])}

AVAILABLE TOOLS:
{self._format_tool_descriptions()}

DECISION FACTORS TO CONSIDER:
1. What specific information or capability do I need next?
2. What has worked or failed in my recent attempts?
3. Am I making progress toward solving the problem?
4. Is my current solution good enough to stop?
5. What would be the most productive next step?

Based on the above context, what should I do next?

Remember:
- Choose tools strategically based on your current needs
- Don't repeat failed approaches without modification
- Consider stopping only if you're truly satisfied
- Be specific about parameters and reasoning
- Focus on making meaningful progress

Your decision:"""
        
        return prompt
    
    def _format_execution_summary(self, exec_summary: Dict[str, Any]) -> str:
        """Format execution summary for the prompt"""
        if exec_summary['executions'] == 0:
            return "No code executions yet"
        
        return f"""- Total executions: {exec_summary['executions']}
- Average quality: {exec_summary['average_quality']:.1f}/100
- Best quality achieved: {exec_summary['best_quality']}/100
- Latest execution quality: {exec_summary['latest_quality']}/100
- Latest exit code: {exec_summary['latest_exit_code']}"""
    
    def _format_tool_descriptions(self) -> str:
        """Format available tools for the LLM"""
        descriptions = []
        for tool_name, schema in self.tool_schemas.items():
            func_info = schema["function"]
            descriptions.append(f"""
{tool_name}:
  Description: {func_info['description']}
  Parameters: {self._format_parameters(func_info['parameters'])}""")
        
        return "\n".join(descriptions)
    
    def _format_parameters(self, params: Dict[str, Any]) -> str:
        """Format parameter information"""
        if "properties" not in params:
            return "No parameters"
        
        param_list = []
        for param_name, param_info in params["properties"].items():
            required = param_name in params.get("required", [])
            req_indicator = " (required)" if required else " (optional)"
            param_list.append(f"{param_name}: {param_info.get('description', 'No description')}{req_indicator}")
        
        return "; ".join(param_list)
    
    def _parse_llm_decision(self, llm_response: str, state: AgentState) -> Dict[str, Any]:
        """Parse LLM response into a structured decision"""
        try:
            # Try to extract JSON from the response
            response_text = llm_response.strip()
            
            # Look for JSON content (might be wrapped in text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                decision = json.loads(json_text)
                
                # Validate the decision structure
                if self._validate_decision(decision, state):
                    return decision
            
            # If JSON parsing fails, try to interpret the response
            return self._interpret_text_response(response_text, state)
            
        except Exception as e:
            state.add_thinking(f"Error parsing LLM decision: {str(e)}")
            return self._get_fallback_decision(state)
    
    def _validate_decision(self, decision: Dict[str, Any], state: AgentState) -> bool:
        """Validate that the decision is properly formatted"""
        if not isinstance(decision, dict):
            return False
        
        action = decision.get("action")
        if action not in ["use_tool", "stop"]:
            return False
        
        if action == "use_tool":
            tool = decision.get("tool")
            if tool not in self.available_tools:
                state.add_thinking(f"Invalid tool requested: {tool}")
                return False
            
            if "parameters" not in decision:
                decision["parameters"] = {}
            
            if "reasoning" not in decision:
                decision["reasoning"] = "No reasoning provided"
        
        elif action == "stop":
            if "reasoning" not in decision:
                decision["reasoning"] = "Agent decided to stop"
        
        return True
    
    def _interpret_text_response(self, response: str, state: AgentState) -> Dict[str, Any]:
        """Try to interpret a non-JSON response"""
        response_lower = response.lower()
        
        # Look for stop indicators
        stop_indicators = ["stop", "satisfied", "complete", "finished", "done"]
        if any(indicator in response_lower for indicator in stop_indicators):
            return {
                "action": "stop",
                "reasoning": f"Interpreted from response: {response[:100]}..."
            }
        
        # Look for tool mentions
        for tool_name in self.available_tools.keys():
            if tool_name in response_lower:
                return {
                    "action": "use_tool",
                    "tool": tool_name,
                    "parameters": {},
                    "reasoning": f"Interpreted {tool_name} from response: {response[:100]}..."
                }
        
        # Default fallback
        return self._get_fallback_decision(state)
    
    def _get_fallback_decision(self, state: AgentState) -> Dict[str, Any]:
        """Provide a sensible fallback decision when LLM response is unclear"""
        
        # If no files exist, start with thinking
        if not state.files_created:
            return {
                "action": "use_tool",
                "tool": "think",
                "parameters": {
                    "focus": "problem analysis",
                    "context": "Starting problem analysis"
                },
                "reasoning": "Fallback: Starting with problem analysis"
            }
        
        # If we have files but no executions, try executing
        if state.files_created and not state.execution_results:
            latest_file = state.files_created[-1]
            if latest_file.filename.endswith('.py'):
                return {
                    "action": "use_tool",
                    "tool": "execute_code",
                    "parameters": {
                        "filename": latest_file.filename,
                        "goal": "test the solution"
                    },
                    "reasoning": "Fallback: Testing the generated solution"
                }
        
        # If quality is low, try thinking about improvements
        if state.best_quality_score < 70:
            return {
                "action": "use_tool",
                "tool": "think",
                "parameters": {
                    "focus": "solution improvement",
                    "context": f"Current quality is {state.best_quality_score}/100"
                },
                "reasoning": "Fallback: Analyzing ways to improve solution quality"
            }
        
        # If we're running out of calls or quality is good, stop
        if state.remaining_calls <= 1 or state.best_quality_score >= 80:
            return {
                "action": "stop",
                "reasoning": f"Fallback: Stopping due to {'call limit' if state.remaining_calls <= 1 else 'good quality achieved'}"
            }
        
        # Last resort - generate code
        return {
            "action": "use_tool",
            "tool": "generate_code",
            "parameters": {
                "approach": "improved solution",
                "based_on": "previous attempts"
            },
            "reasoning": "Fallback: Generating improved solution"
        }
    
    def _build_tool_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Build function calling schemas for all available tools"""
        schemas = {}
        for tool_name, tool_instance in self.available_tools.items():
            schemas[tool_name] = tool_instance.get_schema()
        return schemas
    
    def get_tool_usage_stats(self, state: AgentState) -> Dict[str, Any]:
        """Get statistics about tool usage patterns"""
        tool_counts = {}
        for call in state.tool_calls:
            tool_counts[call.tool_name] = tool_counts.get(call.tool_name, 0) + 1
        
        return {
            "total_calls": len(state.tool_calls),
            "tool_usage": tool_counts,
            "success_rate": sum(1 for call in state.tool_calls if call.success) / max(1, len(state.tool_calls)),
            "most_used_tool": max(tool_counts.items(), key=lambda x: x[1])[0] if tool_counts else None
        }
