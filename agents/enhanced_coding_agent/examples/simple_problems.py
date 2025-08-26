"""
Simple Programming Problems for Enhanced Coding Agent Demo

These problems are designed to test the agent's ability to:
- Understand requirements
- Generate correct solutions
- Create comprehensive tests
- Handle edge cases
"""

SIMPLE_PROBLEMS = {
    "two_sum": {
        "title": "Two Sum Problem",
        "description": """
Write a function that takes a list of integers and a target sum, and returns the indices of two numbers that add up to the target.

Requirements:
- Function should be named 'two_sum'
- Input: list of integers, target integer
- Output: list of two indices [index1, index2]
- Assume exactly one solution exists
- Don't use the same element twice

Example:
- Input: [2, 7, 11, 15], target = 9
- Output: [0, 1] (because 2 + 7 = 9)
""",
        "difficulty": "easy",
        "expected_functions": ["two_sum"],
        "test_cases": [
            {"input": ([2, 7, 11, 15], 9), "output": [0, 1]},
            {"input": ([3, 2, 4], 6), "output": [1, 2]},
            {"input": ([3, 3], 6), "output": [0, 1]}
        ]
    },
    
    "palindrome_check": {
        "title": "Palindrome Checker",
        "description": """
Write a function that checks if a given string is a palindrome (reads the same forwards and backwards).

Requirements:
- Function should be named 'is_palindrome'
- Input: string
- Output: boolean (True if palindrome, False otherwise)
- Ignore case, spaces, and punctuation
- Empty string should return True

Example:
- Input: "A man a plan a canal Panama"
- Output: True
""",
        "difficulty": "easy",
        "expected_functions": ["is_palindrome"],
        "test_cases": [
            {"input": "racecar", "output": True},
            {"input": "A man a plan a canal Panama", "output": True},
            {"input": "race a car", "output": False},
            {"input": "", "output": True},
            {"input": "a", "output": True}
        ]
    },
    
    "fibonacci": {
        "title": "Fibonacci Sequence",
        "description": """
Write a function that returns the nth number in the Fibonacci sequence.

Requirements:
- Function should be named 'fibonacci'
- Input: integer n (0-indexed)
- Output: integer (the nth Fibonacci number)
- Handle edge cases: n=0 returns 0, n=1 returns 1
- Use efficient approach (not naive recursion)

Example:
- Input: 6
- Output: 8 (sequence: 0, 1, 1, 2, 3, 5, 8)
""",
        "difficulty": "easy",
        "expected_functions": ["fibonacci"],
        "test_cases": [
            {"input": 0, "output": 0},
            {"input": 1, "output": 1},
            {"input": 6, "output": 8},
            {"input": 10, "output": 55}
        ]
    },
    
    "word_count": {
        "title": "Word Counter",
        "description": """
Write a function that counts the frequency of each word in a given text.

Requirements:
- Function should be named 'word_count'
- Input: string (text)
- Output: dictionary with word frequencies
- Ignore case (convert to lowercase)
- Remove punctuation
- Handle empty strings

Example:
- Input: "Hello world! Hello Python world."
- Output: {'hello': 2, 'world': 2, 'python': 1}
""",
        "difficulty": "medium",
        "expected_functions": ["word_count"],
        "test_cases": [
            {"input": "hello world", "output": {"hello": 1, "world": 1}},
            {"input": "Hello world! Hello Python world.", "output": {"hello": 2, "world": 2, "python": 1}},
            {"input": "", "output": {}},
            {"input": "test test test", "output": {"test": 3}}
        ]
    },
    
    "list_rotation": {
        "title": "List Rotation",
        "description": """
Write a function that rotates a list to the right by k positions.

Requirements:
- Function should be named 'rotate_list'
- Input: list of elements, integer k (number of positions)
- Output: new rotated list
- Handle cases where k > len(list)
- Handle negative k (rotate left)
- Handle empty lists

Example:
- Input: [1, 2, 3, 4, 5], k=2
- Output: [4, 5, 1, 2, 3]
""",
        "difficulty": "medium",
        "expected_functions": ["rotate_list"],
        "test_cases": [
            {"input": ([1, 2, 3, 4, 5], 2), "output": [4, 5, 1, 2, 3]},
            {"input": ([1, 2, 3], 4), "output": [3, 1, 2]},
            {"input": ([1, 2, 3], -1), "output": [2, 3, 1]},
            {"input": ([], 3), "output": []},
            {"input": ([1], 5), "output": [1]}
        ]
    }
}

def get_problem(problem_name: str) -> dict:
    """Get a specific problem by name"""
    return SIMPLE_PROBLEMS.get(problem_name)

def list_problems() -> list:
    """List all available problem names"""
    return list(SIMPLE_PROBLEMS.keys())

def get_random_problem() -> dict:
    """Get a random problem for testing"""
    import random
    problem_name = random.choice(list_problems())
    return SIMPLE_PROBLEMS[problem_name]

if __name__ == "__main__":
    print("Available Simple Problems:")
    print("=" * 40)
    
    for name, problem in SIMPLE_PROBLEMS.items():
        print(f"\n{problem['title']} ({problem['difficulty']})")
        print(f"Key: {name}")
        print(f"Description: {problem['description'][:100]}...")
        print(f"Expected functions: {problem['expected_functions']}")
        print(f"Test cases: {len(problem['test_cases'])}")
