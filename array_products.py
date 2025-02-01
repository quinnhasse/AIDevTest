from typing import List

def calculate_products(numbers: List[int]) -> List[int]:
    """
    Calculate a list where each element at position i is the product of all numbers
    except the one at position i.

    Args:
        numbers: List of integers

    Returns:
        List of integers where each element is the product of all numbers except
        the one at the corresponding position

    Raises:
        TypeError: If input is None or not a list
        ValueError: If input contains non-integer values

    Examples:
        >>> calculate_products([1, 2, 3, 4])
        [24, 12, 8, 6]
        >>> calculate_products([1, 0, 3, 4])
        [0, 12, 0, 0]
        >>> calculate_products([])
        []
        >>> calculate_products([5])
        [1]
    """
    # Input validation
    if numbers is None:
        raise TypeError("Input cannot be None")
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    if any(not isinstance(x, int) for x in numbers):
        raise ValueError("All elements must be integers")

    # Handle special cases
    n = len(numbers)
    if n == 0:
        return []
    if n == 1:
        return [1]

    # Initialize result array
    result = [1] * n

    # Calculate products of all elements to the left
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= numbers[i]

    # Calculate products of all elements to the right and combine
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= numbers[i]

    return result


if __name__ == "__main__":
    # Example usage
    test_cases = [
        [1, 2, 3, 4],
        [1, 0, 3, 4],
        [],
        [5],
        [2, 3],
    ]
    
    for test in test_cases:
        print(f"Input: {test}")
        print(f"Output: {calculate_products(test)}")
        print()