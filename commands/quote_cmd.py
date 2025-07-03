import requests

# Using Quotable API: https://github.com/lukePeavey/quotable#get-random-quote
API_URL = "https://api.quotable.io/random"
# Alternative: https://type.fit/api/quotes (returns a list, would need to pick one randomly)

def get_random_quote() -> str:
    """
    Fetches a random quote from the Quotable API.
    Returns a formatted string with the quote and author, or an error message.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4XX or 5XX)

        data = response.json()

        if not data or not isinstance(data, dict):
            return "🚫 Error: Received unexpected data format from quote API."

        quote_content = data.get('content')
        quote_author = data.get('author', 'Unknown Author') # Default if author is missing

        if not quote_content:
            return "🚫 Error: Quote content is missing in the API response."

        # Formatting the output
        # Using a simple format, can be made more elaborate
        return f"📜 Random Quote 📜\n\n" \
               f"\"{quote_content}\"\n" \
               f"— {quote_author}"

    except requests.exceptions.HTTPError as http_err:
        # print(f"Quote API HTTP error: {http_err} - {response.text if 'response' in locals() else 'N/A'}")
        return f"🚫 Error: Could not fetch a quote. HTTP {response.status_code if 'response' in locals() else 'Unknown'}."
    except requests.exceptions.RequestException as req_err:
        # print(f"Quote API Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to the quote service."
    except Exception as e:
        # print(f"Quote command error: {e}")
        return f"🚫 Error: An unexpected error occurred while fetching a quote. ({e})"

if __name__ == '__main__':
    print("Testing Random Quote Command:\n")

    # Fetch a few quotes to see variety
    for i in range(3):
        print(f"--- Attempt {i+1} ---")
        quote_message = get_random_quote()
        print(f"{quote_message}\n")
        # Small delay if needed, though this API is usually fast
        if i < 2 and "Error:" not in quote_message :
            import time
            time.sleep(0.2) # Avoid hitting API too rapidly in a loop for testing

    print("Finished quote tests.")
