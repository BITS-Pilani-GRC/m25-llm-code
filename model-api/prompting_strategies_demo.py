import time
import ollama

# Note: Make sure you have Ollama installed and the model pulled:
# 1. Install Ollama: https://ollama.ai/
# 2. Pull the model: ollama pull smollm2:135m
# 3. Verify: ollama list

# We'll use the weak smollm2:135m model to demonstrate how prompting strategies
# can dramatically improve performance of small language models
# MODEL_NAME = "smollm2:135m"
MODEL_NAME = "gpt-oss:latest"

def print_section_header(title):
    """Print a formatted section header for better readability."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def run_prompt(prompt, strategy_name, model=MODEL_NAME):
    """
    Run a prompt using Ollama with smollm2:135m and display the response with timing.
    
    This function demonstrates how different prompting strategies affect the performance
    of a weak language model (135M parameters).
    """
    print(f"\n--- {strategy_name} ---")
    print(f"Model: {model}")
    print(f"Prompt: {prompt}")
    print("\nResponse:")
    
    start_time = time.time()
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{
                'role': 'user', 
                'content': prompt
            }]
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(response['message']['content'])
        print(f"\n[Response time: {response_time:.2f} seconds]")
        print(f"[Model: {model} - 135M parameters]")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running and smollm2:135m is installed:")
        print("  ollama pull smollm2:135m")
    
    print("-" * 60)

def demonstrate_zero_shot():
    """
    ZERO-SHOT PROMPTING
    
    Definition: Asking the model to solve a problem without any examples or guidance.
    
    Expectation with smollm2:135m: 
    - Likely to give wrong answer or show poor reasoning
    - May not follow proper mathematical steps
    - Could provide answers without showing work
    """
    print_section_header("ZERO-SHOT PROMPTING")
    
    print("""
Zero-Shot Prompting:
- No examples provided
- No specific instructions on how to solve
- Tests the model's baseline capability
- Often fails with weak models like smollm2:135m

Expected Issues with Small Models:
- Incorrect calculations
- Poor reasoning steps
- May not show work
""")
    
    prompt = "A store has 24 apples. They sell 8 apples in the morning and 6 apples in the afternoon. How many apples are left?"
    
    run_prompt(prompt, "Zero-Shot")

def demonstrate_few_shot():
    """
    FEW-SHOT PROMPTING
    
    Definition: Providing 2-3 examples of the desired input-output format 
    before asking the model to solve a new problem.
    
    Expectation with smollm2:135m:
    - Should show some improvement in formatting
    - May still struggle with multi-step calculations
    - Examples help the model understand the expected format
    """
    print_section_header("FEW-SHOT PROMPTING")
    
    print("""
Few-Shot Prompting:
- Provides 2-3 examples of similar problems
- Shows the model the expected format and approach
- Helps with pattern recognition
- Should improve performance over zero-shot

Benefits for Small Models:
- Better response formatting
- Understanding of expected output structure
- Pattern matching from examples
""")
    
    prompt = """Here are some examples of how to solve subtraction problems:

Example 1: "A bakery has 15 cookies. They sell 4 cookies. How many are left?"
Answer: "15 - 4 = 11 cookies are left."

Example 2: "A library has 30 books. They lend out 12 books. How many remain?"
Answer: "30 - 12 = 18 books remain."

Now solve this problem:
A garden has 45 flowers. 18 flowers are picked in the morning and 9 flowers are picked in the evening. How many flowers remain in the garden?"""
    
    run_prompt(prompt, "Few-Shot")

def demonstrate_chain_of_thought():
    """
    CHAIN OF THOUGHT (CoT) PROMPTING
    
    Definition: Explicitly asking the model to think step-by-step and show its reasoning process.
    
    Expectation with smollm2:135m:
    - Significant improvement in reasoning quality
    - Step-by-step breakdown helps organize thinking
    - "Think step by step" is a powerful trigger phrase
    """
    print_section_header("CHAIN OF THOUGHT PROMPTING")
    
    print("""
Chain of Thought Prompting:
- Explicitly asks model to "think step by step"
- Encourages showing intermediate reasoning steps
- Helps break down complex problems
- Often dramatically improves weak model performance

Key Phrases:
- "Let's think step by step"
- "Please show your work"
- "Break this down into steps"
""")
    
    prompt = """A rectangular garden is twice as long as it is wide. If the width is 8 meters, and you need to put a fence around the entire garden, how many meters of fence do you need?

Please think step by step."""
    
    run_prompt(prompt, "Chain of Thought")

def demonstrate_prompt_chaining():
    """
    PROMPT CHAINING
    
    Definition: Breaking a complex problem into smaller sub-problems and solving them sequentially,
    using the output of one step as input to the next.
    
    Expectation with smollm2:135m:
    - Dramatic improvement as complex problem is broken into simple parts
    - Each sub-problem is within the model's capability
    - Builds confidence and accuracy through simple steps
    """
    print_section_header("PROMPT CHAINING")
    
    print("""
Prompt Chaining:
- Breaks complex problems into simple sub-problems
- Solves one step at a time
- Uses output from previous step as input to next step
- Transforms impossible problems into manageable ones

Strategy:
1. Identify the complex problem
2. Break it into simple sub-questions
3. Solve each sub-question individually
4. Combine results for final answer
""")
    
    # Step 1
    print("\n🔗 CHAIN STEP 1:")
    step1_prompt = """A school is organizing a field trip. They have 156 students going. Each bus can hold 24 students. How many buses do they need? 

Please just give me the number of buses needed (round up if necessary)."""
    
    run_prompt(step1_prompt, "Chain Step 1: Calculate Buses Needed")
    
    # For demonstration, we'll assume the model gave us 7 buses
    # In a real implementation, you'd parse the response and use it
    buses_needed = 7
    
    # Step 2
    print("\n🔗 CHAIN STEP 2:")
    step2_prompt = f"""Great! They need {buses_needed} buses. Each bus costs $85 to rent for the day. What is the total cost for all buses?

Please just give me the total dollar amount."""
    
    run_prompt(step2_prompt, "Chain Step 2: Calculate Bus Costs")
    
    # Assuming the model calculated $595
    bus_cost = 595
    
    # Step 3
    print("\n🔗 CHAIN STEP 3:")
    step3_prompt = f"""Perfect! The total bus cost is ${bus_cost}. Each student also pays $12 for lunch. With 156 students, what is the total amount collected from all students for lunch?

Please just give me the total dollar amount."""
    
    run_prompt(step3_prompt, "Chain Step 3: Calculate Lunch Money")
    
    # Assuming the model calculated $1,872
    lunch_total = 1872
    
    # Step 4
    print("\n🔗 CHAIN STEP 4:")
    step4_prompt = f"""Excellent! Students pay ${lunch_total} total for lunch. The bus rental costs ${bus_cost}. What is the difference between the total lunch money collected and the total bus rental cost?

Please show me if they have money left over or if they need more money."""
    
    run_prompt(step4_prompt, "Chain Step 4: Calculate Final Difference")
    
    print(f"""
🎯 PROMPT CHAINING SUMMARY:
- Broke complex multi-step problem into 4 simple questions
- Each step builds on the previous one
- Even weak models can handle simple arithmetic
- Final result: Clear understanding of field trip finances

Original Complex Problem:
"Calculate the financial outcome of a field trip with 156 students, buses that hold 24 students costing $85 each, and $12 lunch fees per student."

vs.

Chained Approach:
1. How many buses? (Division)
2. What's the bus cost? (Multiplication) 
3. What's the lunch total? (Multiplication)
4. What's the difference? (Subtraction)
""")

def main():
    """
    Main function to run all prompting strategy demonstrations.
    
    This demo shows how different prompting strategies can dramatically improve
    the performance of weak models like smollm2:135m.
    """
    print_section_header("PROMPTING STRATEGIES DEMO FOR WEAK LLMs")
    
    print("""
🎯 OBJECTIVE: 
Demonstrate how different prompting strategies can dramatically improve the performance 
of weak language models like smollm2:135m (135M parameters).

📝 SETUP REQUIREMENTS:
This demo uses Ollama with smollm2:135m (135M parameter model) to show how prompting 
strategies can dramatically improve weak model performance.

Prerequisites:
1. Ollama installed: https://ollama.ai/
2. Model pulled: ollama pull smollm2:135m  
3. Ollama service running: ollama serve

🔬 WHAT WE'LL EXPLORE:
1. Zero-Shot Prompting (baseline performance)
2. Few-Shot Prompting (learning from examples)  
3. Chain of Thought Prompting (step-by-step reasoning)
4. Prompt Chaining (breaking complex problems down)

Let's see how each strategy progressively improves model performance!
""")
    
    # Run all demonstrations
    demonstrate_zero_shot()
    time.sleep(1)  # Brief pause between sections
    
    demonstrate_few_shot()
    time.sleep(1)
    
    demonstrate_chain_of_thought()
    time.sleep(1)
    
    demonstrate_prompt_chaining()
    time.sleep(1)
    
    print_section_header("DEMO COMPLETE")
    print("""
🎉 CONGRATULATIONS! 

You've seen how prompting strategies can transform weak model performance:
- Zero-shot → Few-shot → Chain of Thought → Prompt Chaining
- Each technique builds upon the previous one
- Even the smallest models can achieve impressive results with proper prompting!

🚀 NEXT STEPS:
1. Experiment with your own problems and domains using smollm2:135m
2. Try combining multiple strategies for even better results
3. Test with other weak models (tinyllama:1.1b, smollm:135m, etc.)
4. Explore advanced prompting techniques (self-consistency, tree of thoughts)

Happy prompting! 🤖✨
""")

if __name__ == "__main__":
    main()