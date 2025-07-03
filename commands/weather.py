import requests # To make HTTP requests to the weather API
from utils.env_loader import get_env_variable # To get API key and bot name

# OpenWeatherMap API details
API_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_icon(icon_code):
    """ Simple mapping from OpenWeatherMap icon codes to emojis. """
    mapping = {
        "01d": "☀️", "01n": "🌙", # Clear sky
        "02d": "🌤️", "02n": "☁️", # Few clouds
        "03d": "☁️", "03n": "☁️", # Scattered clouds
        "04d": "🌥️", "04n": "☁️", # Broken clouds / Overcast clouds
        "09d": "🌧️", "09n": "🌧️", # Shower rain
        "10d": "🌦️", "10n": "🌧️", # Rain
        "11d": "⛈️", "11n": "⛈️", # Thunderstorm
        "13d": "❄️", "13n": "❄️", # Snow
        "50d": "🌫️", "50n": "🌫️", # Mist
    }
    return mapping.get(icon_code, "") # Return emoji or empty string if not found

def fetch_weather_data(location_query: str) -> str:
    """
    Fetches weather data for a given location using OpenWeatherMap API.
    Returns a formatted string with weather information or an error message.
    """
    api_key = get_env_variable("OPENWEATHERMAP_API_KEY")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    # --- DEBUG PRINT ---
    # print(f"DEBUG: Retrieved OPENWEATHERMAP_API_KEY: '{api_key}' (Type: {type(api_key)})") # Commented out
    # --- END DEBUG PRINT ---

    if not api_key or api_key.strip() == "": # More explicit check for empty/whitespace-only key
        return f"🚫 Error: OpenWeatherMap API key is not configured for {bot_name}.\n" \
               f"Please set OPENWEATHERMAP_API_KEY in the .env file. Get one from https://openweathermap.org/appid"

    if not location_query or not location_query.strip():
        return "🚫 Error: No location provided. Usage: /weather <city_name> or /weather <city_name>,<country_code>"

    params = {
        'q': location_query.strip(),
        'appid': api_key,
        'units': 'metric'  # For Celsius. Use 'imperial' for Fahrenheit.
    }

    try:
        response = requests.get(API_BASE_URL, params=params, timeout=10) # 10-second timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        data = response.json()

        # Extracting data (check for existence to avoid KeyErrors if API response structure changes)
        city_name = data.get('name', 'N/A')
        country = data.get('sys', {}).get('country', '')

        weather_info = data.get('weather', [{}])[0] # Get the first weather condition
        description = weather_info.get('description', 'N/A').capitalize()
        icon_code = weather_info.get('icon', '')
        weather_emoji = get_weather_icon(icon_code)

        main_data = data.get('main', {})
        temp = main_data.get('temp', 'N/A')
        feels_like = main_data.get('feels_like', 'N/A')
        humidity = main_data.get('humidity', 'N/A')

        wind_data = data.get('wind', {})
        wind_speed = wind_data.get('speed', 'N/A') # m/s for metric

        # Formatting the output
        location_display = f"{city_name}, {country}" if country else city_name

        weather_report = f"""
        🌤️ **Weather in {location_display}** 🌤️
        -----------------------------------
        {weather_emoji} Condition: {description}
        🌡️ Temperature: {temp}°C
        🤔 Feels like: {feels_like}°C
        💧 Humidity: {humidity}%
        🌬️ Wind Speed: {wind_speed} m/s
        -----------------------------------
        Powered by OpenWeatherMap
        """
        return "\n".join([line.strip() for line in weather_report.strip().split('\n')])


    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            return "🚫 Error: Invalid OpenWeatherMap API key. Please check your .env configuration."
        elif response.status_code == 404:
            return f"🚫 Error: Location '{location_query}' not found. Please check the city name."
        else:
            # print(f"HTTP error occurred: {http_err} - {response.text}") # For logging
            return f"🚫 Error: Could not fetch weather data. HTTP {response.status_code}."
    except requests.exceptions.RequestException as req_err:
        # E.g., DNS failure, connection refused, timeout
        # print(f"Request error occurred: {req_err}") # For logging
        return "🚫 Error: Network problem or could not connect to the weather service."
    except Exception as e:
        # Catch any other unexpected errors, e.g., JSON parsing
        # print(f"An unexpected error occurred in weather command: {e}") # For logging
        return f"🚫 Error: An unexpected error occurred while fetching weather data."

if __name__ == '__main__':
    print("Testing Weather Command (requires OPENWEATHERMAP_API_KEY in .env for full test):\n")

    # Test case 1: API key not set (simulate by temporarily unsetting)
    print("--- Test Case 1: API Key Missing ---")
    original_api_key = os.environ.pop("OPENWEATHERMAP_API_KEY", None) # Temporarily remove if set
    print(f"Output: {fetch_weather_data('London')}\n")
    if original_api_key: # Restore it if it was present
        os.environ["OPENWEATHERMAP_API_KEY"] = original_api_key

    # Test case 2: No location
    print("--- Test Case 2: No Location Provided ---")
    # This test requires API key to be set to pass the initial check,
    # so we assume it might be set by user for their own testing.
    # If not set, it will show the API key error from above.
    if get_env_variable("OPENWEATHERMAP_API_KEY"):
        print(f"Output: {fetch_weather_data('')}\n")
    else:
        print("Skipping 'No Location' test as API key is not set (would show API key error).\n")

    # Test case 3: Valid location (user needs to set API key in .env for this to work)
    print("--- Test Case 3: Valid Location (e.g., 'Paris') ---")
    # This test will only succeed if a valid API key is in the .env file
    if get_env_variable("OPENWEATHERMAP_API_KEY"):
        print(f"Output for Paris: {fetch_weather_data('Paris')}\n")
    else:
        print("Skipping 'Valid Location' test as API key is not set in .env.\n")

    # Test case 4: Invalid/Non-existent location
    print("--- Test Case 4: Invalid Location (e.g., 'NonExistentCity123') ---")
    if get_env_variable("OPENWEATHERMAP_API_KEY"):
        print(f"Output for NonExistentCity123: {fetch_weather_data('NonExistentCity123')}\n")
    else:
        print("Skipping 'Invalid Location' test as API key is not set in .env.\n")

    # Test case 5: Valid location with country code
    print("--- Test Case 5: Valid Location with Country Code (e.g., 'London,UK') ---")
    if get_env_variable("OPENWEATHERMAP_API_KEY"):
        print(f"Output for London,UK: {fetch_weather_data('London,UK')}\n")
    else:
        print("Skipping 'Valid Location with Country Code' test as API key is not set in .env.\n")
