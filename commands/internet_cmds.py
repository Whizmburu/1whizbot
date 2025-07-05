import requests # For GitHub command

# --- Wikipedia Search Command ---
try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

def fetch_wikipedia_summary(query: str = None, sentences: int = 3) -> str:
    """
    Fetches a summary for a given query from Wikipedia.
    """
    if not WIKIPEDIA_AVAILABLE:
        return "🚫 Error: The 'wikipedia' library is not installed. Cannot perform Wikipedia search."

    if not query or not query.strip():
        return "📚 Please provide a search query for Wikipedia. Usage: /wiki <your query>"

    query = query.strip()

    try:
        # Set a default language for summaries if needed, e.g., wikipedia.set_lang("en")
        # For now, it uses the default (usually English).

        # First, try to get a page directly. This helps with specific titles.
        page = wikipedia.page(query, auto_suggest=False, redirect=True) # auto_suggest=False for more precise match first
        summary = wikipedia.summary(page.title, sentences=sentences, auto_suggest=False, redirect=True)
        page_url = page.url

        return f"📖 **{page.title}**\n\n{summary}\n\n🔗 Read more: {page_url}"

    except wikipedia.exceptions.PageError:
        # If exact page not found, try searching and suggest options
        search_results = wikipedia.search(query, results=3)
        if search_results:
            suggestions = "\n - ".join(search_results)
            return f"😕 Page for '{query}' not found. Did you mean one of these?\n - {suggestions}\nTry `/wiki <suggestion>`."
        else:
            return f"😕 Sorry, no Wikipedia page found for '{query}' and no suggestions available."

    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n - ".join(e.options[:5]) # Show first 5 disambiguation options
        return f"🚧 '{query}' refers to multiple topics (disambiguation):\n - {options}\n" \
               f"Please be more specific or try one of the options above with `/wiki <option>`."

    except requests.exceptions.RequestException as net_err: # wikipedia lib uses requests
        # print(f"Wikipedia network error: {net_err}")
        return "🚫 Error: Could not connect to Wikipedia. Please check your internet connection."
    except Exception as e:
        # print(f"Wikipedia command error: {e}")
        return f"🚫 Error: An unexpected error occurred while searching Wikipedia. ({e})"

# --- GitHub User Info Command ---
GITHUB_API_URL = "https://api.github.com/users/"

def fetch_github_user_info(username: str = None) -> str:
    """
    Fetches profile information for a given GitHub username.
    """
    if not username or not username.strip():
        return "👤 Please provide a GitHub username. Usage: /github <username>"

    username_to_lookup = username.strip()

    try:
        response = requests.get(f"{GITHUB_API_URL}{username_to_lookup}", timeout=10)

        if response.status_code == 404:
            return f"😕 GitHub user '{username_to_lookup}' not found."

        response.raise_for_status() # Raise HTTPError for other bad responses

        data = response.json()

        # Extracting key information
        login = data.get('login', 'N/A')
        name = data.get('name', login) # Use login if name is not set
        bio = data.get('bio', 'No bio provided.')
        public_repos = data.get('public_repos', 0)
        followers = data.get('followers', 0)
        following = data.get('following', 0)
        profile_url = data.get('html_url', 'N/A')
        avatar_url = data.get('avatar_url', '') # For potential future image display
        created_at_str = data.get('created_at', 'N/A')

        # Format created_at date if available
        if created_at_str != 'N/A':
            try:
                from dateutil import parser as date_parser # For robust date parsing
                created_date = date_parser.parse(created_at_str)
                created_at_formatted = created_date.strftime('%Y-%m-%d')
            except ImportError: # Fallback if dateutil is not available (it was installed with python-whois)
                created_at_formatted = created_at_str.split('T')[0] # Simple YYYY-MM-DD
            except Exception:
                created_at_formatted = created_at_str # Fallback to raw string if parsing fails
        else:
            created_at_formatted = "N/A"

        # Constructing the message
        # (Avatar URL can be sent as an image separately in a real bot)
        info = f"""
        👤 **GitHub Profile: {name} ({login})**
        -----------------------------------
        📝 Bio: {bio if bio else "Not specified."}
        Repositories: {public_repos}
        Followers: {followers} | Following: {following}
        Joined GitHub: {created_at_formatted}
        🔗 Profile URL: {profile_url}
        """
        # Avatar: {avatar_url} (Could be sent as image)

        return "\n".join([line.strip() for line in info.strip().split('\n')])

    except requests.exceptions.HTTPError as http_err:
        # print(f"GitHub API HTTP error: {http_err} - {response.text}")
        return f"🚫 Error: Could not fetch GitHub profile. HTTP {response.status_code}."
    except requests.exceptions.RequestException as req_err:
        # print(f"GitHub API Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to GitHub API."
    except Exception as e:
        # print(f"GitHub command error: {e}")
        return f"🚫 Error: An unexpected error occurred while fetching GitHub profile. ({e})"


if __name__ == '__main__':
    print("--- Testing Internet Commands ---\n")

    print("Testing Wikipedia Search:")
    if WIKIPEDIA_AVAILABLE:
        test_queries = [
            "Python programming language",
            "Artificial Intelligence",
            "Whiz-MD Bot", # Likely not found
            "Apple", # Might be disambiguation
            "", # Empty query
            "Jupiter", # Planet
            "sdlkfjsdlfkjsdlfkj" # Gibberish
        ]
        for i, q_str in enumerate(test_queries):
            print(f"--- Wiki Test {i+1}: '{q_str}' ---")
            result = fetch_wikipedia_summary(q_str)
            print(f"{result}\n")
    else:
        print("  Wikipedia library not available, skipping tests.")
    print("-" * 20 + "\n")

    print("Testing GitHub User Info:")
    # python-dateutil should be available as it's a dependency of python-whois
    test_github_users = [
        "octocat", # Standard GitHub test user
        "WHIZ-MD", # Assuming this user exists
        "nonexistentgithubuser12345xyz", # Should not exist
        "", # Empty username
    ]
    for i, user in enumerate(test_github_users):
        print(f"--- GitHub Test {i+1}: '{user}' ---")
        result_gh = fetch_github_user_info(user)
        print(f"{result_gh}\n")
    print("-" * 20 + "\n")
