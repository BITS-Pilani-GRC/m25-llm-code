def calculate_circle_area(radius):
    """Calculate the area of a circle"""
    # Bug: Missing ** 2 for radius squared
    return 3.14159 * radius

def calculate_rectangle_area(length, width):
    """Calculate the area of a rectangle"""
    # Bug: Using multiplication instead of addition
    return length * width * 2

def find_average(numbers):
    """Find the average of a list of numbers"""
    if len(numbers) == 0:
        return 0
    # Bug: Not dividing by count
    total = sum(numbers)
    return total

def is_even(number):
    """Check if a number is even"""
    # Bug: Wrong condition
    return number % 2 == 1

if __name__ == "__main__":
    print("Testing functions:")
    print(f"Circle area (radius=5): {calculate_circle_area(5)} (should be ~78.54)")
    print(f"Rectangle area (4x6): {calculate_rectangle_area(4, 6)} (should be 24)")
    print(f"Average of [1,2,3,4,5]: {find_average([1,2,3,4,5])} (should be 3)")
    print(f"Is 4 even? {is_even(4)} (should be True)")
    print(f"Is 7 even? {is_even(7)} (should be False)")
