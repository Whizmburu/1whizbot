import pyshorteners
import re

# Basic URL validation regex (simplified)
# Checks for http/https prefix and some domain characters.
# For robust validation, a more comprehensive regex or library would be better.
URL_PATTERN = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def generate_short_url(long_url_str: str) -> str:
    """
    Shortens a given URL using TinyURL.
    Returns a message string with the short URL or an error message.
    """
    if not long_url_str or not long_url_str.strip():
        return "🚫 Error: No URL provided. Usage: /shorturl <your_long_url>"

    # Validate the URL format (basic check)
    if not URL_PATTERN.match(long_url_str.strip()):
        return f"🚫 Error: Invalid URL format provided: '{long_url_str}'. Please include http:// or https://."

    try:
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(long_url_str.strip())

        return f"✅ URL shortened successfully!\n" \
               f"🔗 Original: {long_url_str}\n" \
               f"🤏 Shortened: {short_url}"

    except pyshorteners.exceptions.ShorteningErrorException as e:
        # This can happen if the service is down or the URL is rejected by the service
        # print(f"TinyURL API error: {e}") # For logging
        return f"🚫 Error: The URL shortening service (TinyURL) could not process the request. It might be an invalid URL for the service or a temporary issue. ({e})"
    except Exception as e:
        # Catch other potential errors (e.g., network issues with 'requests' library)
        # print(f"URL shortening error: {e}") # For logging
        return f"🚫 Error: Could not shorten URL. An unexpected error occurred. ({e})"

if __name__ == '__main__':
    test_urls = [
        "https://www.google.com",
        "http://github.com/WHIZ-MD/Bot",
        "https://www.averylongdomainnameexample.com/with/some/very/long/path/and/query?params=true&another=value",
        "ftp://example.com/resource", # FTP (check if tinyurl supports - often not)
        "not_a_url",
        "www.google.com", # Missing scheme
        "", # Empty string
        "https://already_short_url.t.co", # Already shortened (should still work)
    ]

    print("Testing URL shortening function:\n")
    for i, url in enumerate(test_urls):
        print(f"Input {i+1}: '{url}'")
        result_message = generate_short_url(url)
        print(f"  Output: {result_message}\n")

    # Test with a known problematic URL for some shorteners (e.g. localhost, though TinyURL might handle it)
    print(f"Input: 'http://localhost:8000'")
    result_message_localhost = generate_short_url('http://localhost:8000')
    print(f"  Output: {result_message_localhost}\n")

    print(f"Input: 'http://127.0.0.1/test'")
    result_message_ip = generate_short_url('http://127.0.0.1/test')
    print(f"  Output: {result_message_ip}\n")
