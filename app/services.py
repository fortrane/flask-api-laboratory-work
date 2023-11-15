import numpy as np


def convert_to_base13(num):
    if not isinstance(num, int) or num < 0:
        return None

    if num == 0:
        return "0"

    digits = "0123456789ABC"
    result = ""
    while num > 0:
        result = digits[num % 13] + result
        num = num // 13

    return result


def multiply_matrix_scalar(matrix, scalar):
    try:
        return [[element * scalar for element in row] for row in matrix]
    except TypeError as e:
        return f"Error: {str(e)}"


def solve_quadratic_equation(a, b, c):
    roots = np.roots([a, b, c])
    return [round(root.real, 2) if root.imag == 0 else str(root) for root in roots]


def remove_vowels(text):
    vowels = "aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ"
    return ''.join([char for char in text if char not in vowels])