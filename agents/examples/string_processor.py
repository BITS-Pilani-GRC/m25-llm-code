def count_words(text):
    """Count the number of words in text"""
    if not text or text.strip() == "":
        return 0
    words = text.split()
    return len(words)

def reverse_words(text):
    """Reverse the order of words in text"""
    words = text.split()
    reversed_words = words[::-1]
    return " ".join(reversed_words)

def capitalize_first_letter(text):
    """Capitalize the first letter of each word"""
    words = text.split()
    capitalized = []
    for word in words:
        if len(word) > 0:
            capitalized.append(word[0].upper() + word[1:].lower())
    return " ".join(capitalized)

if __name__ == "__main__":
    test_text = "hello world python programming"
    
    print("Testing string functions:")
    print(f"Original: '{test_text}'")
    print(f"Word count: {count_words(test_text)}")
    print(f"Reversed: '{reverse_words(test_text)}'")
    print(f"Capitalized: '{capitalize_first_letter(test_text)}'")
    
    print("\nEdge cases:")
    print(f"Empty string word count: {count_words('')}")
    print(f"Single word reversed: '{reverse_words('hello')}')")
