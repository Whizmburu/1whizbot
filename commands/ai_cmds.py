import os
from utils.env_loader import get_env_variable

# --- OpenAI Ask Command ---
try:
    from openai import OpenAI, APIError, AuthenticationError, RateLimitError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    # Define dummy exceptions if openai is not available for type hinting or isinstance checks
    class APIError(Exception): pass
    class AuthenticationError(Exception): pass
    class RateLimitError(Exception): pass


def get_ai_response(user_prompt: str = None) -> str:
    """
    Gets a response from OpenAI's chat completion API based on the user's prompt.
    """
    if not OPENAI_AVAILABLE:
        return "🚫 Error: The 'openai' library is not installed. Cannot use AI features."

    api_key = get_env_variable("OPENAI_API_KEY")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD") # For system message or error messages

    if not api_key or not api_key.startswith("sk-"): # Basic check for API key format
        return f"🚫 Error: OpenAI API key is not configured or invalid for {bot_name}.\n" \
               f"Please set a valid OPENAI_API_KEY (starting with 'sk-') in the .env file."

    if not user_prompt or not user_prompt.strip():
        return "🤖 Please provide a prompt or question for the AI. Usage: /ask <your question>"

    try:
        # The OpenAI client automatically picks up OPENAI_API_KEY from env variables
        client = OpenAI()

        # Default system message can be customized
        system_message = f"You are {bot_name}, a helpful AI assistant integrated into a multi-purpose bot. Keep your responses concise and informative."

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or choose another model like "gpt-4" if available/preferred
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt.strip()}
            ],
            max_tokens=250, # Limit response length to keep it manageable for chat
            temperature=0.7 # A balance between creativity and determinism
        )

        ai_reply = chat_completion.choices[0].message.content

        if not ai_reply or not ai_reply.strip():
            return "🤔 The AIpondered for a moment but didn't have a specific answer. Try rephrasing your question!"

        return f"🤖 **{bot_name} AI says:**\n\n{ai_reply.strip()}"

    except AuthenticationError:
        return "🚫 Error: OpenAI API Key is invalid or has insufficient permissions. Please check your key."
    except RateLimitError:
        return "🚫 Error: OpenAI API rate limit exceeded. Please try again later or check your usage."
    except APIError as e: # More general OpenAI API errors
        # print(f"OpenAI APIError: {e}")
        return f"🚫 Error: An issue occurred with the OpenAI API. (Status: {e.status_code}, Message: {e.message})"
    except Exception as e: # Catch-all for other issues like network problems with the openai client
        # print(f"AI command error: {e}")
        return f"🚫 Error: An unexpected error occurred while communicating with the AI. ({e})"


if __name__ == '__main__':
    print("--- Testing AI Commands ---\n")

    print("Testing AI Ask Command (/ask):")
    # These tests require a valid OPENAI_API_KEY in .env
    # Simulate API key check first
    original_openai_key = get_env_variable("OPENAI_API_KEY")

    print("  --- Test Case 1: OpenAI API Key Missing (simulated) ---")
    if original_openai_key:
        # To truly test this, we'd need to ensure os.environ['OPENAI_API_KEY'] is unset
        # For now, we'll assume get_env_variable correctly reflects .env
        # Let's simulate by setting it to an invalid format for the check in get_ai_response
        os.environ["OPENAI_API_KEY"] = "INVALID_KEY_FORMAT"
    print(f"  Output (invalid key format): {get_ai_response('What is the capital of France?')}\n")
    if original_openai_key: # Restore it if it was present
         os.environ["OPENAI_API_KEY"] = original_openai_key
    else: # If it was never set, remove the temp invalid one
        if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"] == "INVALID_KEY_FORMAT":
            del os.environ["OPENAI_API_KEY"]


    print("  --- Test Case 2: No Prompt ---")
    print(f"  Output (no prompt): {get_ai_response('')}\n")

    if original_openai_key and original_openai_key.startswith("sk-"):
        print("  --- Test Case 3: Valid Prompt (requires valid API key in .env) ---")
        print(f"  Output for 'What is 2+2?':\n{get_ai_response('What is 2+2?')}\n")

        print("  --- Test Case 4: Another Valid Prompt ---")
        print(f"  Output for 'Explain black holes simply':\n{get_ai_response('Explain black holes simply for a child')}\n")
    else:
        print("  Skipping further OpenAI tests as OPENAI_API_KEY is not set or invalid in .env.\n")

    print("-" * 20 + "\n")
