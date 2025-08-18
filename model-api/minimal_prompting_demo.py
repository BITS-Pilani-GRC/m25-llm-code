import ollama

MODEL_NAME = "gpt-oss:latest"

def run_prompt(prompt, technique_name):
    """Run prompt and display response."""
    print(f"\n--- {technique_name} ---")
    print(f"Prompt: {prompt}")
    print("Response:")
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        print(response['message']['content'])
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 50)

def zero_shot():
    """Zero-shot: Direct question without examples."""
    prompt = "What are the main causes of climate change?"
    run_prompt(prompt, "Zero-Shot")

def few_shot():
    """Few-shot: Provide examples before the main question."""
    prompt = """Classify the sentiment of these movie reviews:

Review: "The plot was confusing and the acting felt forced."
Sentiment: Negative

Review: "Brilliant cinematography and outstanding performances by the entire cast."
Sentiment: Positive

Review: "It was okay, nothing special but not terrible either."
Sentiment: Neutral

Now classify this review:
Review: "The movie had great visuals but the story was disappointing."
Sentiment:"""
    run_prompt(prompt, "Few-Shot")

def chain_of_thought():
    """Chain of thought: Ask for step-by-step reasoning."""
    prompt = """A restaurant has 12 tables. Each table can seat 4 people. If the restaurant is 75% full, how many people are dining?

Think step by step."""
    run_prompt(prompt, "Chain of Thought")

def json_output():
    """JSON format: Request structured output."""
    prompt = """Analyze this sentence: "The quick brown fox jumps over the lazy dog"

Return your analysis in JSON format with these fields:
- word_count
- has_all_letters (boolean)
- longest_word
- sentence_type"""
    run_prompt(prompt, "JSON Output Format")

if __name__ == "__main__":
    zero_shot()
    few_shot()
    chain_of_thought()
    json_output()
