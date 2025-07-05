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

# --- News Command (NewsAPI.org) ---
NEWS_API_BASE_URL = "https://newsapi.org/v2/top-headlines"
# Supported countries and categories can be extensive.
# For simplicity, we'll allow common ones and default.
# Full list: https://newsapi.org/docs/endpoints/top-headlines (sources endpoint for categories/countries)
NEWS_DEFAULT_COUNTRY = "us"
NEWS_DEFAULT_CATEGORY = "general" # Other e.g., business, entertainment, health, science, sports, technology
NEWS_DEFAULT_COUNT = 5

def fetch_top_headlines(country: str = NEWS_DEFAULT_COUNTRY,
                        category: str = NEWS_DEFAULT_CATEGORY,
                        count: int = NEWS_DEFAULT_COUNT) -> str:
    """
    Fetches top news headlines from NewsAPI.org.
    """
    from utils.env_loader import get_env_variable # Delayed import

    api_key = get_env_variable("NEWSAPI_ORG_API_KEY")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    if not api_key or api_key.strip() == "":
        return f"🚫 Error: NewsAPI.org API key is not configured for {bot_name}.\n" \
               f"Please set NEWSAPI_ORG_API_KEY in the .env file. Get one from https://newsapi.org"

    params = {
        'country': country.lower() if country else NEWS_DEFAULT_COUNTRY,
        'category': category.lower() if category else NEWS_DEFAULT_CATEGORY,
        'apiKey': api_key,
        'pageSize': count
    }

    try:
        response = requests.get(NEWS_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status() # Raises HTTPError for bad responses

        data = response.json()

        if data.get("status") != "ok":
            return f"🚫 Error from NewsAPI: {data.get('code')} - {data.get('message', 'Unknown API error')}"

        articles = data.get("articles", [])
        if not articles:
            return f"😕 No news articles found for country '{params['country']}' and category '{params['category']}'."

        output_parts = [f"📰 Top {len(articles)} Headlines ({params['country'].upper()}, {params['category'].capitalize()}):"]
        output_parts.append("-----------------------------------")

        for i, article in enumerate(articles):
            title = article.get('title', 'No Title')
            source_name = article.get('source', {}).get('name', 'Unknown Source')
            url = article.get('url', '#')
            # description = article.get('description', '') # Optional: add description
            output_parts.append(f"{i+1}. {title} (Source: {source_name})\n   🔗 {url}")

        output_parts.append("-----------------------------------")
        output_parts.append("Powered by NewsAPI.org")

        return "\n".join(output_parts)

    except requests.exceptions.HTTPError as http_err:
        # print(f"NewsAPI HTTP error: {http_err} - {response.text}")
        if response.status_code == 401: # Unauthorized
             return "🚫 Error: Invalid NewsAPI.org API key. Please check .env configuration."
        elif response.status_code == 429: # Too Many Requests
             return "🚫 Error: NewsAPI.org rate limit exceeded. Please try again later."
        return f"🚫 Error: Could not fetch news. HTTP {response.status_code}."
    except requests.exceptions.RequestException as req_err:
        # print(f"NewsAPI Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to the news service."
    except Exception as e:
        # print(f"News command error: {e}")
        return f"🚫 Error: An unexpected error occurred while fetching news. ({e})"


if __name__ == '__main__':
    print("--- Testing Internet Commands ---\n")

    print("Testing Wikipedia Search:")
    if WIKIPEDIA_AVAILABLE:
        # ... (wiki tests remain the same)
        print(f"  Wiki for 'Python programming language' (snippet):\n{fetch_wikipedia_summary('Python programming language')[:200]}...\n")
    else:
        print("  Wikipedia library not available, skipping tests.")
    print("-" * 20 + "\n")

    print("Testing GitHub User Info:")
    # ... (github tests remain the same)
    print(f"  GitHub for 'octocat':\n{fetch_github_user_info('octocat')}\n")
    print("-" * 20 + "\n")

    print("Testing News Headlines:")
    # These tests require NEWSAPI_ORG_API_KEY in .env
    # Simulate API key check first
    from utils.env_loader import get_env_variable
    original_news_api_key = get_env_variable("NEWSAPI_ORG_API_KEY")

    print("  --- Test Case 1: News API Key Missing (simulated) ---")
    if original_news_api_key:
        import os
        del os.environ["NEWSAPI_ORG_API_KEY"] # Temporarily remove for test
    print(f"  Output (no key): {fetch_top_headlines()}\n")
    if original_news_api_key: # Restore if it was present
         os.environ["NEWSAPI_ORG_API_KEY"] = original_news_api_key

    if original_news_api_key: # Only run further tests if key was originally present
        print("  --- Test Case 2: Default News (US, General) ---")
        print(f"  Output: {fetch_top_headlines()}\n")

        print("  --- Test Case 3: News for GB, Technology ---")
        print(f"  Output: {fetch_top_headlines(country='gb', category='technology', count=3)}\n")

        print("  --- Test Case 4: News for invalid country 'xx' ---")
        # NewsAPI might return an error or empty list for invalid params
        print(f"  Output: {fetch_top_headlines(country='xx')}\n")
    else:
        print("  Skipping further NewsAPI tests as NEWSAPI_ORG_API_KEY is not set in .env.\n")
    print("-" * 20 + "\n")

# --- NPM Package Info Command ---
NPM_API_BASE_URL = "https://registry.npmjs.org/"

def fetch_npm_package_info(package_name: str = None) -> str:
    """
    Fetches information about a given NPM package.
    """
    if not package_name or not package_name.strip():
        return "📦 Please provide an NPM package name. Usage: /npm <package_name>"

    # NPM package names can be scoped, e.g., @angular/core.
    # The API endpoint needs URL encoding for the slash in scoped packages.
    # However, requests library usually handles URL encoding of path segments if they are part of the URL string.
    # Let's ensure the package_name itself is safe for a URL path component.
    # For scoped packages, the API path is like: registry.npmjs.org/@angular%2Fcore
    # A simple replace should work if requests doesn't auto-encode the slash in the path.
    # Or, use urllib.parse.quote_plus for the package_name part of the URL.
    # For requests, it's often better to let it handle path params if possible, or build carefully.
    # Let's try simple join first. `requests` should handle it.

    package_name_to_lookup = package_name.strip()
    # Scoped packages like @babel/core - the API expects the slash NOT url-encoded in the path part.
    # Example: https://registry.npmjs.org/@babel/core

    try:
        response = requests.get(f"{NPM_API_BASE_URL}{package_name_to_lookup}", timeout=10)

        if response.status_code == 404:
            return f"😕 NPM package '{package_name_to_lookup}' not found."

        response.raise_for_status()
        data = response.json()

        name = data.get('name', 'N/A')
        description = data.get('description', 'No description provided.')
        latest_version = data.get('dist-tags', {}).get('latest', 'N/A')
        license_info = data.get('license', 'N/A')
        homepage_url = data.get('homepage', 'N/A')
        # Other useful fields: `maintainers`, `keywords`, `repository.url`

        # Format created_at and modified_at from time field
        time_data = data.get('time', {})
        created_at_raw = time_data.get('created', 'N/A')
        modified_at_raw = time_data.get('modified', 'N/A')

        created_at_fmt = "N/A"
        modified_at_fmt = "N/A"

        try:
            from dateutil import parser as date_parser
            if created_at_raw != 'N/A':
                created_at_fmt = date_parser.parse(created_at_raw).strftime('%Y-%m-%d')
            if modified_at_raw != 'N/A':
                modified_at_fmt = date_parser.parse(modified_at_raw).strftime('%Y-%m-%d')
        except ImportError: # Fallback if dateutil not present
            if created_at_raw != 'N/A': created_at_fmt = created_at_raw.split('T')[0]
            if modified_at_raw != 'N/A': modified_at_fmt = modified_at_raw.split('T')[0]
        except Exception: # Catch parsing errors for dates
            if created_at_raw != 'N/A': created_at_fmt = created_at_raw
            if modified_at_raw != 'N/A': modified_at_fmt = modified_at_raw


        info = f"""
        📦 **NPM Package: {name}**
        -----------------------------------
        📝 Description: {description}
        🏷️ Version: {latest_version}
        📜 License: {license_info}
        🏠 Homepage: {homepage_url if homepage_url != 'N/A' else 'Not specified'}
        📅 Created: {created_at_fmt}
        🔄 Last Modified: {modified_at_fmt}
        -----------------------------------
        Data from registry.npmjs.org
        """
        return "\n".join([line.strip() for line in info.strip().split('\n')])

    except requests.exceptions.HTTPError as http_err:
        # print(f"NPM API HTTP error: {http_err} - {response.text}")
        return f"🚫 Error: Could not fetch NPM package info. HTTP {response.status_code}."
    except requests.exceptions.RequestException as req_err:
        # print(f"NPM API Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to NPM registry."
    except Exception as e:
        # print(f"NPM command error: {e}")
        return f"🚫 Error: An unexpected error occurred while fetching NPM package info. ({e})"


if __name__ == '__main__':
    print("--- Testing Internet Commands ---\n")

    print("Testing Wikipedia Search:")
    # ... (wiki tests remain the same)
    if WIKIPEDIA_AVAILABLE:
        print(f"  Wiki for 'Python programming language' (snippet):\n{fetch_wikipedia_summary('Python programming language')[:200]}...\n")
    else:
        print("  Wikipedia library not available, skipping tests.")
    print("-" * 20 + "\n")

    print("Testing GitHub User Info:")
    # ... (github tests remain the same)
    print(f"  GitHub for 'octocat':\n{fetch_github_user_info('octocat')}\n")
    print("-" * 20 + "\n")

    print("Testing News Headlines:")
    # ... (news tests remain the same, ensure NEWSAPI_ORG_API_KEY check)
    from utils.env_loader import get_env_variable # For __main__ test section
    if get_env_variable("NEWSAPI_ORG_API_KEY"):
        print(f"  News (default):\n{fetch_top_headlines(count=1)}\n") # Fetch 1 for brevity
    else:
        print("  NEWSAPI_ORG_API_KEY not set, skipping NewsAPI tests in __main__.\n")
    print("-" * 20 + "\n")

    print("Testing NPM Package Info:")
    test_npm_packages = [
        "lodash",
        "react",
        "@angular/core", # Scoped package
        "nonexistentnpmpackage12345xyz", # Should not exist
        "", # Empty package name
    ]
    for i, pkg_name in enumerate(test_npm_packages):
        print(f"--- NPM Test {i+1}: '{pkg_name}' ---")
        result_npm = fetch_npm_package_info(pkg_name)
        print(f"{result_npm}\n")
    print("-" * 20 + "\n")

# --- Movie Info Command (OMDB API) ---
OMDB_API_URL = "http://www.omdbapi.com/"

def fetch_movie_details(movie_title: str = None) -> str:
    """
    Fetches details for a given movie title using OMDB API.
    """
    from utils.env_loader import get_env_variable # Delayed import

    api_key = get_env_variable("OMDB_API_KEY")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    if not api_key or api_key.strip() == "":
        return f"🚫 Error: OMDB API key is not configured for {bot_name}.\n" \
               f"Please set OMDB_API_KEY in the .env file. Get one from http://www.omdbapi.com/apikey.aspx"

    if not movie_title or not movie_title.strip():
        return "🎬 Please provide a movie title to search. Usage: /movie <title>"

    params = {
        't': movie_title.strip(),
        'apikey': api_key,
        'plot': 'short' # Or 'full'
    }

    try:
        response = requests.get(OMDB_API_URL, params=params, timeout=10)
        response.raise_for_status() # Raises HTTPError for bad responses like 5xx

        data = response.json()

        if data.get("Response") == "False":
            error_message = data.get("Error", "Movie not found or API error.")
            if "Movie not found!" in error_message:
                 return f"😕 Movie '{movie_title}' not found. Please check the title."
            return f"🚫 Error from OMDB API: {error_message}"

        # Extracting key information
        title = data.get('Title', 'N/A')
        year = data.get('Year', 'N/A')
        rated = data.get('Rated', 'N/A')
        released = data.get('Released', 'N/A')
        runtime = data.get('Runtime', 'N/A')
        genre = data.get('Genre', 'N/A')
        director = data.get('Director', 'N/A')
        writer = data.get('Writer', 'N/A')
        actors = data.get('Actors', 'N/A')
        plot = data.get('Plot', 'N/A')
        language = data.get('Language', 'N/A')
        country = data.get('Country', 'N/A')
        awards = data.get('Awards', 'N/A')
        imdb_rating = data.get('imdbRating', 'N/A')
        metascore = data.get('Metascore', 'N/A')
        poster_url = data.get('Poster', '') # For potential future image display

        info = f"""
        🎬 **{title} ({year})**
        -----------------------------------
        Rated: {rated} | Runtime: {runtime} | Released: {released}
        Genre: {genre}
        Director: {director}
        Writer(s): {writer}
        Actors: {actors}
        Language: {language} | Country: {country}
        -----------------------------------
        **Plot:** {plot}
        -----------------------------------
        🏆 Awards: {awards}
        ⭐ IMDb Rating: {imdb_rating}/10
        Ⓜ️ Metascore: {metascore}/100
        """
        # Poster: {poster_url} (Could be sent as image)

        return "\n".join([line.strip() for line in info.strip().split('\n')])

    except requests.exceptions.HTTPError as http_err:
        # print(f"OMDB API HTTP error: {http_err} - {response.text}")
        if response.status_code == 401: # Unauthorized (invalid API key)
             return "🚫 Error: Invalid OMDB API key. Please check .env configuration."
        return f"🚫 Error: Could not fetch movie details. HTTP {response.status_code}."
    except requests.exceptions.RequestException as req_err:
        # print(f"OMDB API Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to the movie database service."
    except Exception as e:
        # print(f"Movie command error: {e}")
        return f"🚫 Error: An unexpected error occurred while fetching movie details. ({e})"


if __name__ == '__main__':
    print("--- Testing Internet Commands ---\n")

    # ... (previous tests for wiki, github, news remain the same) ...
    print("Testing Wikipedia Search:")
    if WIKIPEDIA_AVAILABLE:
        print(f"  Wiki for 'Python programming language' (snippet):\n{fetch_wikipedia_summary('Python programming language')[:100]}...\n")
    else:
        print("  Wikipedia library not available, skipping tests.")
    print("-" * 20 + "\n")

    print("Testing GitHub User Info:")
    print(f"  GitHub for 'octocat':\n{fetch_github_user_info('octocat')[:100]}...\n")
    print("-" * 20 + "\n")

    from utils.env_loader import get_env_variable # For __main__ test section
    print("Testing News Headlines:")
    if get_env_variable("NEWSAPI_ORG_API_KEY"):
        print(f"  News (default snippet):\n{fetch_top_headlines(count=1)}\n")
    else:
        print("  NEWSAPI_ORG_API_KEY not set, skipping NewsAPI tests in __main__.\n")
    print("-" * 20 + "\n")

    print("Testing NPM Package Info:")
    print(f"  NPM for 'react' (snippet):\n{fetch_npm_package_info('react')[:100]}...\n")
    print("-" * 20 + "\n")

    print("Testing Movie Info:")
    original_omdb_key = get_env_variable("OMDB_API_KEY")
    print("  --- Test Case 1: OMDB API Key Missing (simulated) ---")
    if original_omdb_key:
        import os
        del os.environ["OMDB_API_KEY"]
    print(f"  Output (no key): {fetch_movie_details('Inception')}\n")
    if original_omdb_key:
        os.environ["OMDB_API_KEY"] = original_omdb_key # Restore

    if original_omdb_key:
        print("  --- Test Case 2: Valid Movie Title ('Inception') ---")
        print(f"  Output: {fetch_movie_details('Inception')}\n")

        print("  --- Test Case 3: Movie Not Found ('NonExistentMovieTitle123') ---")
        print(f"  Output: {fetch_movie_details('NonExistentMovieTitle123')}\n")

        print("  --- Test Case 4: No Movie Title ---")
        print(f"  Output: {fetch_movie_details('')}\n")
    else:
        print("  Skipping further OMDB tests as OMDB_API_KEY is not set in .env.\n")
    print("-" * 20 + "\n")

# --- Anime Search Command (Jikan API) ---
JIKAN_API_URL = "https://api.jikan.moe/v4/anime"

def search_jikan_anime(anime_query: str = None, limit: int = 1) -> str:
    """
    Searches for anime information using the Jikan API (MyAnimeList).
    Fetches the first result.
    """
    if not anime_query or not anime_query.strip():
        return "🌸 Please provide an anime title or query to search. Usage: /anime <query>"

    params = {
        'q': anime_query.strip(),
        'limit': limit,
        # 'sfw': True # Optionally filter for SFW results if desired by default
    }

    try:
        response = requests.get(JIKAN_API_URL, params=params, timeout=15) # Jikan can sometimes be slower
        response.raise_for_status() # Raises HTTPError for bad responses

        data = response.json()

        results = data.get("data", [])
        if not results or not isinstance(results, list) or len(results) == 0:
            return f"😕 No anime found matching '{anime_query}'. Please try a different query."

        anime_data = results[0] # Get the first result

        title = anime_data.get('title', 'N/A')
        title_english = anime_data.get('title_english', title) # Fallback to main title
        title_japanese = anime_data.get('title_japanese', 'N/A')

        anime_type = anime_data.get('type', 'N/A')
        episodes = anime_data.get('episodes', 'N/A')
        status = anime_data.get('status', 'N/A')
        score = anime_data.get('score', 'N/A')
        rating = anime_data.get('rating', 'N/A') # Age rating like PG-13

        synopsis_raw = anime_data.get('synopsis', 'No synopsis available.')
        # Shorten synopsis if too long
        max_synopsis_len = 250
        synopsis = (synopsis_raw[:max_synopsis_len] + '...') if synopsis_raw and len(synopsis_raw) > max_synopsis_len else synopsis_raw

        url = anime_data.get('url', 'N/A')
        image_url = anime_data.get('images', {}).get('jpg', {}).get('image_url', '') # For future image display

        info = f"""
        🌸 **{title_english if title_english else title}** ({title_japanese}) 🌸
        -----------------------------------
        Type: {anime_type} | Episodes: {episodes} | Status: {status}
        ⭐ Score: {score}/10 | Rating: {rating}
        -----------------------------------
        **Synopsis:**
        {synopsis}
        -----------------------------------
        🔗 More Info: {url}
        """
        # Image: {image_url} (Could be sent as image)

        return "\n".join([line.strip() for line in info.strip().split('\n')])

    except requests.exceptions.HTTPError as http_err:
        # print(f"Jikan API HTTP error: {http_err} - {response.text}")
        # Jikan API might return 429 for rate limiting if hit too often
        if response.status_code == 404: # Should be caught by no results, but as a fallback
             return f"😕 No anime found for '{anime_query}' (API 404)."
        elif response.status_code == 429:
             return "🚫 Error: Jikan API rate limit hit. Please try again in a moment."
        return f"🚫 Error: Could not fetch anime data from Jikan API. HTTP {response.status_code}."
    except requests.exceptions.RequestException as req_err:
        # print(f"Jikan API Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to the Jikan API service."
    except Exception as e:
        # print(f"Anime command error: {e}")
        return f"🚫 Error: An unexpected error occurred while searching for anime. ({e})"


if __name__ == '__main__':
    print("--- Testing Internet Commands ---\n")

    # ... (previous tests for wiki, github, news, npm, movie remain the same) ...
    print("Testing Wikipedia Search:")
    if WIKIPEDIA_AVAILABLE:
        print(f"  Wiki for 'Python programming language' (snippet):\n{fetch_wikipedia_summary('Python programming language')[:100]}...\n")
    else:
        print("  Wikipedia library not available, skipping tests.")
    print("-" * 20 + "\n")

    print("Testing GitHub User Info:")
    print(f"  GitHub for 'octocat':\n{fetch_github_user_info('octocat')[:100]}...\n")
    print("-" * 20 + "\n")

    from utils.env_loader import get_env_variable # For __main__ test section
    print("Testing News Headlines:")
    if get_env_variable("NEWSAPI_ORG_API_KEY"):
        print(f"  News (default snippet):\n{fetch_top_headlines(count=1)}\n")
    else:
        print("  NEWSAPI_ORG_API_KEY not set, skipping NewsAPI tests in __main__.\n")
    print("-" * 20 + "\n")

    print("Testing NPM Package Info:")
    print(f"  NPM for 'react' (snippet):\n{fetch_npm_package_info('react')[:100]}...\n")
    print("-" * 20 + "\n")

    print("Testing Movie Info:")
    if get_env_variable("OMDB_API_KEY"):
        print(f"  Movie 'Inception' (snippet):\n{fetch_movie_details('Inception')[:150]}...\n")
    else:
        print("  OMDB_API_KEY not set, skipping Movie tests in __main__.\n")
    print("-" * 20 + "\n")

    print("Testing Anime Search (Jikan API):")
    test_anime_queries = [
        "Naruto",
        "Attack on Titan",
        "Your Name", # Movie
        "NonExistentAnimeTitle123XYZ", # Should not exist
        "", # Empty query
    ]
    for i, query in enumerate(test_anime_queries):
        print(f"--- Anime Test {i+1}: '{query}' ---")
        result_anime = search_jikan_anime(query)
        print(f"{result_anime}\n")
    print("-" * 20 + "\n")
