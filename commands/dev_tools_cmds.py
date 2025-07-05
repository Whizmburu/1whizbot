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

# --- WHOIS Lookup Command ---
import datetime # Import the standard datetime module
try:
    import whois
    # from whois.parser import PywhoisError # Specific error type
    PYTHON_WHOIS_AVAILABLE = True
except ImportError:
    PYTHON_WHOIS_AVAILABLE = False
    # class PywhoisError(Exception): pass # Define for type hinting if needed
    # class whois: pass # Dummy class if whois is not available, to prevent NameError on whois.datetime below.
                       # This is not ideal, better to guard access to whois.datetime.

def format_whois_value(value):
    """Helper to format WHOIS values, especially dates and lists."""
    if isinstance(value, list):
        # If all items are datetime objects, format them
        # Ensure whois is available before trying to access whois.datetime
        if PYTHON_WHOIS_AVAILABLE and all(isinstance(item, datetime.datetime) for item in value): # Corrected: datetime.datetime
            return ", ".join([item.strftime('%Y-%m-%d %H:%M:%S UTC') for item in value])
        return ", ".join(map(str, value)) # Join list elements as strings
    elif PYTHON_WHOIS_AVAILABLE and isinstance(value, datetime.datetime): # Corrected: datetime.datetime
        return value.strftime('%Y-%m-%d %H:%M:%S UTC')
    return str(value) if value is not None else "N/A"

def fetch_whois_data(domain_name: str = None) -> str:
    """
    Fetches WHOIS information for a given domain name.
    """
    if not PYTHON_WHOIS_AVAILABLE:
        return "🚫 Error: The 'python-whois' library is not installed. Cannot perform WHOIS lookup."

    if not domain_name or not domain_name.strip():
        return "🚫 Error: No domain name provided. Usage: /whois <domain_name>"

    domain_to_lookup = domain_name.strip().lower()
    # Basic sanity check for domain format, though whois library might handle variations.
    # A simple check: does it contain at least one dot and no spaces?
    if " " in domain_to_lookup or "." not in domain_to_lookup:
        return f"🚫 Error: Invalid domain format: '{domain_name}'. Please provide a valid domain (e.g., example.com)."

    try:
        w = whois.whois(domain_to_lookup)

        if not w or not w.domain_name: # Check if any result was returned or if domain_name is empty
             # Sometimes python-whois returns an empty result for domains not found or certain TLDs
             # Or if the domain_name attribute itself is None or empty after query
            if hasattr(w, 'text') and w.text: # If there's raw text, it might mean no structured data
                 # This case is tricky, as w.text might exist even for successful lookups.
                 # The library's behavior for "not found" can vary.
                 # Let's assume if w.domain_name is missing, it's likely a "not found" or unsupported TLD.
                return f"ℹ️ WHOIS lookup for '{domain_to_lookup}' did not return structured data or the domain may not exist.\n" \
                       f"   Raw output snippet (first 500 chars):\n```\n{w.text[:500]}...\n```"
            return f"🚫 Error: Could not retrieve WHOIS data for '{domain_to_lookup}'. Domain may not exist or WHOIS server unavailable."

        # Format the output
        # Key attributes to display. The python-whois library normalizes many of these.
        key_info = {
            "Domain Name": w.domain_name, # Often a list
            "Registrar": w.registrar,
            "WHOIS Server": w.whois_server,
            "Referral URL": w.referral_url, # Usually for the registrar
            "Updated Date": w.updated_date,
            "Creation Date": w.creation_date,
            "Expiration Date": w.expiration_date,
            "Name Servers": w.name_servers, # List
            "Status": w.status, # List or string
            "Emails": w.emails, # List
            "DNSSEC": w.dnssec,
            "Registrant Name": w.name, # Registrant's name
            "Organization": w.org, # Registrant's organization
            "Address": w.address,
            "City": w.city,
            "State": w.state,
            "Zipcode": w.zipcode,
            "Country": w.country,
        }

        output_parts = [f"🔍 WHOIS Information for: {format_whois_value(w.domain_name)}"]
        output_parts.append("-----------------------------------")

        for key, value in key_info.items():
            if value is not None: # Only show fields that have a value
                formatted_value = format_whois_value(value)
                if formatted_value != "N/A" and formatted_value.strip() != "": # Check if value is actually useful
                    output_parts.append(f"🔹 {key}: {formatted_value}")

        output_parts.append("-----------------------------------")
        output_parts.append("Note: WHOIS data can vary by registrar and TLD.")

        return "\n".join(output_parts)

    except whois.parser.PywhoisError as e: # Catch errors from the whois library itself
        # This can include "No match for..." or other parsing issues.
        return f"🚫 Error: WHOIS lookup failed for '{domain_to_lookup}'. Domain may not exist or no WHOIS entry found. ({e})"
    except Exception as e:
        # print(f"WHOIS command error: {e}") # For logging
        return f"🚫 Error: An unexpected error occurred during WHOIS lookup for '{domain_to_lookup}'. ({e})"


if __name__ == '__main__':
    print("--- Testing Dev Tools Commands ---\n")

    print("Testing Base64:")
    # ... (base64 tests remain the same)
    print(f"  Encode 'Hello World': {handle_base64('encode', 'Hello World')}")
    print(f"  Decode 'SGVsbG8gV29ybGQ=': {handle_base64('decode', 'SGVsbG8gV29ybGQ=')}")
    print(f"  Decode (invalid base64 string '!!!'): {handle_base64('decode', '!!!')}")
    print("-" * 20 + "\n")

    print("Testing JSON Formatter:")
    # ... (jsonfmt tests remain the same)
    valid_json_compact = '{"name": "Whiz-MD", "version": 1.0, "features": ["utility", "fun", {"text": "tools"}], "active": true}'
    print(f"  Valid compact JSON: {format_json_string(valid_json_compact)}")
    print("-" * 20 + "\n")

    print("Testing WHOIS Lookup:")
    if PYTHON_WHOIS_AVAILABLE:
        test_domains = [
            "google.com",
            "github.com",
            "nonexistentdomain123xyz.com", # Should fail or return no data
            "example.org",
            "", # Empty input
            "invalid domain", # Invalid format
            "faketld.thistlddoesnotexist"
        ]
        for i, domain in enumerate(test_domains):
            print(f"--- WHOIS Test {i+1}: '{domain}' ---")
            result = fetch_whois_data(domain)
            print(f"{result}\n")
    else:
        print("  python-whois library not available, skipping WHOIS tests.")
    print("-" * 20 + "\n")

# --- DNS Lookup Command ---
try:
    import dns.resolver
    import dns.exception
    DNSPYTHON_AVAILABLE = True
    SUPPORTED_RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "CNAME", "NS", "SOA", "SRV", "PTR"] # Common types
except ImportError:
    DNSPYTHON_AVAILABLE = False
    SUPPORTED_RECORD_TYPES = []
    # Define dummy exceptions if dnspython is not available, for type hinting or isinstance checks
    # class dns:
    #     class resolver: class NXDOMAIN(Exception): pass; class NoAnswer(Exception): pass; class Timeout(Exception): pass
    #     class exception: class DNSException(Exception): pass


def format_dns_answer(answer, record_type):
    """Helper to format different DNS record types."""
    record_type = record_type.upper()
    if record_type == "A":
        return answer.address
    elif record_type == "AAAA":
        return answer.address
    elif record_type == "MX":
        return f"{answer.preference} {answer.exchange.to_text(omit_final_dot=True)}"
    elif record_type == "TXT":
        # TXT records can be list of bytes strings, join them
        return " ".join(b.decode('utf-8') for b in answer.strings)
    elif record_type == "CNAME":
        return answer.target.to_text(omit_final_dot=True)
    elif record_type == "NS":
        return answer.target.to_text(omit_final_dot=True)
    elif record_type == "SOA": # More complex, just show main parts
        return f"MNAME: {answer.mname.to_text(omit_final_dot=True)}, RNAME: {answer.rname.to_text(omit_final_dot=True)}, Serial: {answer.serial}"
    elif record_type == "SRV":
        return f"{answer.priority} {answer.weight} {answer.port} {answer.target.to_text(omit_final_dot=True)}"
    elif record_type == "PTR":
        return answer.target.to_text(omit_final_dot=True)
    return str(answer) # Fallback

def fetch_dns_records(domain_name: str = None, record_type: str = "A") -> str:
    """
    Fetches DNS records for a given domain name and record type.
    """
    if not DNSPYTHON_AVAILABLE:
        return "🚫 Error: The 'dnspython' library is not installed. Cannot perform DNS lookup."

    if not domain_name or not domain_name.strip():
        return "🚫 Error: No domain name provided. Usage: /dns <domain_name> [record_type]"

    domain_to_lookup = domain_name.strip().lower()
    req_record_type = record_type.strip().upper() if record_type else "A"

    if req_record_type not in SUPPORTED_RECORD_TYPES:
        return f"🚫 Error: Unsupported DNS record type '{req_record_type}'. Supported types: {', '.join(SUPPORTED_RECORD_TYPES)}"

    try:
        answers = dns.resolver.resolve(domain_to_lookup, req_record_type)

        if not answers: # Should be caught by NoAnswer, but as a safeguard
            return f"ℹ️ No {req_record_type} records found for '{domain_to_lookup}'."

        output_parts = [f"🔍 DNS {req_record_type} Records for: {domain_to_lookup}"]
        output_parts.append("-----------------------------------")

        for rdata in answers:
            output_parts.append(f"  🔹 {format_dns_answer(rdata, req_record_type)}")

        if not output_parts[2:]: # If only header and separator, means no records were formatted (shouldn't happen if answers exist)
             return f"ℹ️ No {req_record_type} records found or could not format for '{domain_to_lookup}'."

        return "\n".join(output_parts)

    except dns.resolver.NXDOMAIN:
        return f"🚫 Error: Domain '{domain_to_lookup}' does not exist (NXDOMAIN)."
    except dns.resolver.NoAnswer:
        return f"ℹ️ No {req_record_type} records found for '{domain_to_lookup}'."
    except dns.resolver.Timeout:
        return f"🚫 Error: DNS query for '{domain_to_lookup}' [{req_record_type}] timed out."
    except dns.exception.DNSException as e: # Catch other dnspython specific exceptions
        # print(f"DNS lookup error (DNSException): {e}")
        return f"🚫 Error during DNS lookup for '{domain_to_lookup}' [{req_record_type}]: {e}"
    except Exception as e:
        # print(f"DNS command error: {e}")
        return f"🚫 Error: An unexpected error occurred during DNS lookup. ({e})"


if __name__ == '__main__':
    print("--- Testing Dev Tools Commands ---\n")

    print("Testing Base64:")
    # ... (base64 tests remain the same)
    print(f"  Encode 'Hello World': {handle_base64('encode', 'Hello World')}")
    print(f"  Decode 'SGVsbG8gV29ybGQ=': {handle_base64('decode', 'SGVsbG8gV29ybGQ=')}")
    print(f"  Decode (invalid base64 string '!!!'): {handle_base64('decode', '!!!')}")
    print("-" * 20 + "\n")

    print("Testing JSON Formatter:")
    # ... (jsonfmt tests remain the same)
    valid_json_compact = '{"name": "Whiz-MD", "version": 1.0, "features": ["utility", "fun", {"text": "tools"}], "active": true}'
    print(f"  Valid compact JSON: {format_json_string(valid_json_compact)}")
    print("-" * 20 + "\n")

    print("Testing WHOIS Lookup:")
    # ... (whois tests remain the same, ensuring PYTHON_WHOIS_AVAILABLE check)
    if PYTHON_WHOIS_AVAILABLE:
        print(f"  WHOIS for google.com (snippet):\n{fetch_whois_data('google.com')[:200]}...\n")
    else:
        print("  python-whois library not available, skipping WHOIS tests.")
    print("-" * 20 + "\n")

    print("Testing DNS Lookup:")
    if DNSPYTHON_AVAILABLE:
        test_dns_queries = [
            ("google.com", "A"),
            ("google.com", "AAAA"),
            ("google.com", "MX"),
            ("google.com", "TXT"),
            ("google.com", "NS"),
            ("www.google.com", "CNAME"), # Might be A/AAAA directly
            ("gmail.com", "MX"),
            ("_sip._tcp.google.com", "SRV"), # Example SRV record
            ("nonexistentdomain123xyz.com", "A"),
            ("google.com", "PTR"), # PTR usually for IPs
            ("google.com", "SOA"),
            ("google.com", "INVALIDTYPE"),
            ("", "A"), # No domain
        ]
        for i, (domain, rtype) in enumerate(test_dns_queries):
            print(f"--- DNS Test {i+1}: '{domain}' [{rtype}] ---")
            result = fetch_dns_records(domain, rtype)
            print(f"{result}\n")
    else:
        print("  dnspython library not available, skipping DNS tests.")
    print("-" * 20 + "\n")
