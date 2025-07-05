import base64
import binascii # For catching specific base64 decoding errors

# --- Base64 Encode/Decode Command ---
def handle_base64(action: str, input_string: str = None) -> str:
    """
    Encodes or decodes a string using Base64.
    Action: "encode" or "decode".
    """
    if not action or action.lower() not in ["encode", "decode"]:
        return "🚫 Error: Invalid action. Usage: /base64 <encode|decode> <string>"

    if not input_string or not input_string.strip():
        return f"🚫 Error: No string provided to {action}. Usage: /base64 {action} <string>"

    action = action.lower()
    input_string = input_string.strip()

    try:
        if action == "encode":
            message_bytes = input_string.encode('utf-8')
            base64_bytes = base64.b64encode(message_bytes)
            encoded_string = base64_bytes.decode('utf-8')
            return f"🔒 Base64 Encoded:\n```\n{encoded_string}\n```"

        elif action == "decode":
            # Ensure the input string is valid for base64 decoding (padding, characters)
            # The library itself will raise an error for incorrect padding or chars.
            base64_bytes = input_string.encode('utf-8') # Input should be ASCII/UTF-8 for b64 chars
            message_bytes = base64.b64decode(base64_bytes)
            try:
                decoded_string = message_bytes.decode('utf-8')
                return f"🔓 Base64 Decoded:\n```\n{decoded_string}\n```"
            except UnicodeDecodeError:
                return "🚫 Error: Decoded data is not valid UTF-8. It might be binary data."

    except binascii.Error as b64_error: # Specific error for invalid base64 string
        return f"🚫 Error: Invalid Base64 string provided for decoding. ({b64_error})"
    except Exception as e:
        # print(f"Base64 error: {e}") # For logging
        return f"🚫 Error during Base64 {action}: {e}"

if __name__ == '__main__':
    print("--- Testing Dev Tools Commands ---\n")

    print("Testing Base64:")
    # Encode tests
    print(f"  Encode 'Hello World': {handle_base64('encode', 'Hello World')}")
    print(f"  Encode 'Whiz-MD Bot!': {handle_base64('encode', 'Whiz-MD Bot!')}")
    print(f"  Encode (empty string): {handle_base64('encode', ' ')}") # Test with whitespace only
    print(f"  Encode (no string): {handle_base64('encode')}")

    # Decode tests
    # SGVsbG8gV29ybGQ= is "Hello World"
    print(f"  Decode 'SGVsbG8gV29ybGQ=': {handle_base64('decode', 'SGVsbG8gV29ybGQ=')}")
    # V2hp blowoutLW1EIEJvdCE= is "Whiz-MD Bot!"
    print(f"  Decode 'V2hp blowoutLW1EIEJvdCE=': {handle_base64('decode', 'V2hp blowoutLW1EIEJvdCE=')}")
    print(f"  Decode (invalid base64 string '!!!'): {handle_base64('decode', '!!!')}")
    print(f"  Decode (incorrect padding 'SGVsbG8'): {handle_base64('decode', 'SGVsbG8')}")
    print(f"  Decode (no string): {handle_base64('decode')}")

    # Invalid action
    print(f"  Invalid action 'scramble': {handle_base64('scramble', 'test')}")
    print(f"  No action: {handle_base64(None, 'test')}")

    # Test decoding non-UTF-8 binary data (represented as b64)
    # Example: b'\x80\x81\x82' encoded to base64 is 'gIGC'
    binary_b64 = "gIGC"
    print(f"  Decode binary data '{binary_b64}': {handle_base64('decode', binary_b64)}")

    print("-" * 20 + "\n")

# --- JSON Formatter Command ---
import json

def format_json_string(json_input_str: str = None) -> str:
    """
    Formats a JSON string with indentation.
    """
    if not json_input_str or not json_input_str.strip():
        return "🚫 Error: No JSON string provided. Usage: /jsonfmt <json_string>"

    try:
        # Attempt to parse the JSON string
        parsed_json = json.loads(json_input_str.strip())

        # Re-serialize it with indentation (e.g., 2 spaces)
        formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False) # ensure_ascii=False for unicode chars

        return f"✨ Formatted JSON:\n```json\n{formatted_json}\n```"

    except json.JSONDecodeError as e:
        return f"🚫 Error: Invalid JSON string provided.\n   Details: {e.msg} (line {e.lineno} column {e.colno})"
    except Exception as e:
        # print(f"JSON format error: {e}") # For logging
        return f"🚫 Error: Could not format JSON. ({e})"


if __name__ == '__main__':
    print("--- Testing Dev Tools Commands ---\n")

    print("Testing Base64:")
    # ... (base64 tests remain the same)
    print(f"  Encode 'Hello World': {handle_base64('encode', 'Hello World')}")
    print(f"  Decode 'SGVsbG8gV29ybGQ=': {handle_base64('decode', 'SGVsbG8gV29ybGQ=')}")
    print(f"  Decode (invalid base64 string '!!!'): {handle_base64('decode', '!!!')}")
    print("-" * 20 + "\n")

    print("Testing JSON Formatter:")
    valid_json_compact = '{"name": "Whiz-MD", "version": 1.0, "features": ["utility", "fun", {"text": "tools"}], "active": true}'
    valid_json_with_unicode = '{"name": "Whiz-MD", "greeting": "你好世界"}'
    invalid_json_syntax = '{"name": "Whiz-MD", "version": 1.0, features: ["utility"]}' # Missing quotes around features key
    invalid_json_trailing_comma = '{"name": "Whiz-MD", "version": 1.0,}'

    print(f"  Valid compact JSON: {format_json_string(valid_json_compact)}")
    print(f"\n  Valid JSON with Unicode: {format_json_string(valid_json_with_unicode)}")
    print(f"\n  Invalid JSON (syntax error): {format_json_string(invalid_json_syntax)}")
    print(f"\n  Invalid JSON (trailing comma): {format_json_string(invalid_json_trailing_comma)}")
    print(f"\n  Empty input: {format_json_string('')}")
    print(f"\n  None input: {format_json_string(None)}")
    print(f"\n  Non-JSON string: {format_json_string('Just some random text')}")
    print("-" * 20 + "\n")
