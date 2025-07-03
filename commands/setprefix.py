import re

# Basic validation: prefixes should not contain whitespace and should not be empty.
# They also shouldn't be excessively long, e.g. > 5 chars.
# For simplicity, we'll just check for non-empty and no whitespace.
MIN_PREFIX_LEN = 1
MAX_PREFIX_LEN = 5 # Arbitrary reasonable max length for a prefix

def validate_prefix(prefix):
    """Validates a single prefix."""
    if not (MIN_PREFIX_LEN <= len(prefix) <= MAX_PREFIX_LEN):
        return False, f"Prefix '{prefix}' length must be between {MIN_PREFIX_LEN} and {MAX_PREFIX_LEN} characters."
    if re.search(r"\s", prefix): # Check for whitespace
        return False, f"Prefix '{prefix}' cannot contain whitespace."
    # Add any other character restrictions if needed, e.g., alphanumeric only
    # if not prefix.isalnum() and not all(c in ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '='] for c in prefix):
    #    return False, f"Prefix '{prefix}' contains invalid characters."
    return True, ""

def update_prefix_list(new_prefixes_str):
    """
    Parses the new prefixes string, validates them, and returns a new list
    of prefixes along with a status message.
    Returns: (list_of_new_prefixes_or_None, status_message_str)
    """
    if not new_prefixes_str or new_prefixes_str.strip() == "":
        return None, "🚫 Error: No prefixes provided. Please specify one or more prefixes separated by spaces."

    potential_new_prefixes = new_prefixes_str.strip().split()
    validated_prefixes = []
    error_messages = []

    if not potential_new_prefixes: # Should be caught by above, but as a safeguard
        return None, "🚫 Error: No prefixes provided after parsing."

    for p_str in potential_new_prefixes:
        is_valid, msg = validate_prefix(p_str)
        if is_valid:
            if p_str not in validated_prefixes: # Avoid duplicates
                validated_prefixes.append(p_str)
        else:
            error_messages.append(msg)

    if error_messages:
        # If any prefix is invalid, reject the whole set for now for simplicity.
        # Alternatively, one could accept valid ones and report errors for others.
        return None, "🚫 Error validating prefixes:\n" + "\n".join(error_messages)

    if not validated_prefixes: # All provided prefixes were invalid or duplicates that became empty
        return None, "🚫 Error: No valid prefixes found after validation."

    prefix_display_str = " | ".join(f'"{p}"' for p in validated_prefixes)
    return validated_prefixes, f"✅ Prefixes updated successfully to: {prefix_display_str}"

if __name__ == '__main__':
    # Test cases
    print("Testing prefix updates:\n")

    test_cases = [
        "",
        "   ",
        "/ . !",
        "new",
        "a b c d e f", # Test multiple, some potentially valid
        "toolongprefix / short", # One too long, one valid
        "valid whitespace invalid", # One with whitespace
        "ok another_ok",
        "!@# ok", # Some special chars
        "/ / . !", # Duplicates
        "x y z"
    ]

    for case in test_cases:
        print(f"Input: '{case}'")
        new_list, message = update_prefix_list(case)
        if new_list:
            print(f"  Result: New list: {new_list}")
        print(f"  Message: {message}\n")

    print("Test with only invalid prefixes:")
    new_list_invalid, message_invalid = update_prefix_list("toolong one two three")
    print(f"  Message: {message_invalid}\n")

    print("Test with only valid prefixes (duplicates):")
    new_list_valid_dup, message_valid_dup = update_prefix_list("/ / . !")
    print(f"  New List: {new_list_valid_dup}")
    print(f"  Message: {message_valid_dup}\n")
