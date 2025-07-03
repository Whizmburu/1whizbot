import re
import math # For allowing math constants like pi and e, and functions if desired later

# Define allowed characters and patterns for sanitization
# This allows numbers, basic arithmetic operators, parentheses, and whitespace.
# It also allows a decimal point.
ALLOWED_CHARS_PATTERN = re.compile(r"^[0-9\s\.\+\-\*\/\%\(\)\^\/\/\*\*]+$")

# For more advanced math, one might want to allow specific math functions or constants.
# For now, we keep it to basic arithmetic.
# A safer alternative to eval is using ast.literal_eval for simple literals,
# or a full math expression parser like 'numexpr' or 'asteval'.
# For this exercise, we'll use a regex-sanitized eval.

def evaluate_expression(expression_string: str) -> str:
    """
    Safely evaluates a mathematical expression string.
    Returns the result as a string or an error message.
    """
    if not expression_string:
        return "🚫 Error: No expression provided."

    # Sanitize the input string
    # 1. Remove any characters not in the allowed set (basic safety)
    # A stricter approach would be to reject if any invalid char is found.
    # Let's try rejecting first.
    if not ALLOWED_CHARS_PATTERN.match(expression_string):
        # Find the offending characters for a more helpful message (optional)
        # offending_chars = "".join(sorted(list(set(re.sub(ALLOWED_CHARS_PATTERN, "", expression_string)))))
        # return f"🚫 Error: Expression contains invalid characters: {offending_chars}"
        return "🚫 Error: Expression contains invalid characters. Only numbers, operators (+-*/%**//^), and parentheses are allowed."

    # Replace ^ with ** for Python exponentiation if user uses ^
    expression_to_eval = expression_string.replace('^', '**')

    # Further checks (e.g., prevent very long expressions, multiple consecutive operators not handled by eval)
    if len(expression_to_eval) > 100: # Arbitrary limit
        return "🚫 Error: Expression is too long."

    try:
        # Eval in a restricted environment (though direct eval is still risky)
        # For basic arithmetic, the regex above should make it relatively safe.
        # __builtins__ can be restricted further for eval.
        # result = eval(expression_to_eval, {"__builtins__": {}}, {}) # Too restrictive, no math ops
        # A slightly safer eval environment:
        safe_globals = {
            "__builtins__": {}, # Remove most builtins
            "abs": abs, "round": round, "pow": pow,
            # Add math constants if desired, ensure they are not overwritten by user input
            # "pi": math.pi, "e": math.e
        }
        # Note: Direct eval is powerful. The regex is the primary defense here.
        # Libraries like asteval are much safer for untrusted input.
        result = eval(expression_to_eval, safe_globals, {})

        # Check if result is a number (int, float)
        if not isinstance(result, (int, float)):
            return "🚫 Error: Evaluation did not result in a number."

        return f"💡 Result: {result}"
    except ZeroDivisionError:
        return "🚫 Error: Division by zero."
    except SyntaxError:
        return "🚫 Error: Invalid syntax in expression."
    except TypeError:
        return "🚫 Error: Type error in expression (e.g., mismatched types for operation)."
    except Exception as e:
        # Catch-all for other potential eval issues
        # print(f"Calculator eval error: {e}") # For logging/debugging
        return f"🚫 Error: Could not evaluate expression."


if __name__ == '__main__':
    test_expressions = [
        "2 + 2",
        "10 - 5.5",
        "3 * 7",
        "100 / 4",
        "10 // 3", # Integer division
        "10 % 3",  # Modulo
        "2 ** 5",  # Exponentiation
        "2 ^ 5",   # Alternative exponentiation
        "(10 + 2) * 3",
        "1 / 0",   # Division by zero
        "1 +",     # Syntax error
        "import os", # Invalid characters / attempt to exploit (should be caught by regex)
        "print('hello')", # Invalid characters
        "a + 5", # Invalid characters
        "abs(-5)", # Allowed if abs is in safe_globals
        "pow(2,3)", # Allowed if pow is in safe_globals
        "round(3.14159, 2)", # Allowed if round is in safe_globals
        "   5 *    (2+1)   ", # With spaces
        "1.0 / 3.0",
        " ".join(["1"]*50) + "+" + " ".join(["1"]*50) # Very long expression
    ]

    print("Testing expression evaluation:\n")
    for expr in test_expressions:
        print(f"Input: '{expr}'")
        output = evaluate_expression(expr)
        print(f"  Output: {output}\n")

    print("Test with empty input:")
    print(f"  Output: {evaluate_expression('')}\n")

    print("Test with only invalid chars:")
    print(f"Input: 'foo_bar'")
    print(f"  Output: {evaluate_expression('foo_bar')}\n")

    print("Test with mixed valid/invalid (should fail):")
    print(f"Input: '5 + five'")
    print(f"  Output: {evaluate_expression('5 + five')}\n")

    print("Test for max length:")
    long_expr = "1+"*60 + "1"
    print(f"Input: (long expression of length {len(long_expr)})")
    print(f" Output: {evaluate_expression(long_expr)}\n")

    short_long_expr = "1+"*40 + "1"
    print(f"Input: (expression of length {len(short_long_expr)})")
    print(f" Output: {evaluate_expression(short_long_expr)}\n")
