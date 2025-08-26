def mystery_function(x, y):
    """A mysterious mathematical function"""
    result = x * y + x
    return result

def another_function(numbers):
    """Process a list of numbers"""
    total = 0
    for num in numbers:
        if num > 0:
            total += num * 2
        else:
            total += num
    return total

if __name__ == "__main__":
    print("Testing mystery function:")
    print(f"mystery_function(3, 4) = {mystery_function(3, 4)}")
    print(f"mystery_function(2, 5) = {mystery_function(2, 5)}")
    
    print("\nTesting another function:")
    test_numbers = [1, -2, 3, -4, 5]
    print(f"another_function({test_numbers}) = {another_function(test_numbers)}")