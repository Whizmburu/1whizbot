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

# --- AI Image Generation Command ---
def generate_ai_image_from_prompt(prompt: str = None,
                                  n: int = 1,
                                  size: str = "1024x1024",
                                  model: str = "dall-e-2") -> str: # dall-e-2 is cheaper and faster for general use
    """
    Generates an image using OpenAI's DALL·E model based on a prompt.
    Returns a string with the image URL(s) or an error message.
    """
    if not OPENAI_AVAILABLE:
        return "🚫 Error: The 'openai' library is not installed. Cannot use AI image generation."

    api_key = get_env_variable("OPENAI_API_KEY")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    if not api_key or not api_key.startswith("sk-"):
        return f"🚫 Error: OpenAI API key is not configured or invalid for {bot_name}.\n" \
               f"Please set a valid OPENAI_API_KEY (starting with 'sk-') in the .env file."

    if not prompt or not prompt.strip():
        return "🖼️ Please provide a prompt to generate an image! Usage: /imagegen <your image description>"

    # Validate size parameter against DALL·E-2 supported sizes
    # DALL·E 2 supports 256x256, 512x512, 1024x1024
    # DALL·E 3 supports 1024x1024, 1792x1024, 1024x1792 (and has different 'quality' and 'style' params)
    # For now, sticking to DALL·E 2 compatible sizes for simplicity if model="dall-e-2"
    valid_sizes_dalle2 = ["256x256", "512x512", "1024x1024"]
    valid_sizes_dalle3 = ["1024x1024", "1792x1024", "1024x1792"] # DALL-E 3 also has quality and style params

    chosen_model = model
    chosen_size = size

    if chosen_model == "dall-e-2" and chosen_size not in valid_sizes_dalle2:
        # print(f"Warning: Invalid size '{chosen_size}' for DALL·E 2. Defaulting to '1024x1024'.")
        chosen_size = "1024x1024" # Default or error out
    elif chosen_model == "dall-e-3" and chosen_size not in valid_sizes_dalle3:
        # print(f"Warning: Invalid size '{chosen_size}' for DALL·E 3. Defaulting to '1024x1024'.")
        chosen_size = "1024x1024"

    # n must be between 1 and 10 for DALL-E 2. DALL-E 3 currently only supports n=1.
    if chosen_model == "dall-e-3" and n > 1:
        # print("Warning: DALL-E 3 only supports n=1. Setting n to 1.")
        n = 1
    elif n < 1 or n > 10: # General cap for DALL-E 2
        # print(f"Warning: Number of images (n={n}) out of range [1-10]. Defaulting to 1.")
        n = 1


    try:
        client = OpenAI()

        response = client.images.generate(
            model=chosen_model,
            prompt=prompt.strip(),
            n=n,
            size=chosen_size,
            response_format="url" # b64_json is also an option
        )

        image_urls = [img.url for img in response.data if img.url]

        if not image_urls:
            return "🖼️ The AI tried, but couldn't generate an image for that prompt. Maybe try something different?"

        result_message = f"🎨 Here's your AI-generated image{'s' if len(image_urls) > 1 else ''} based on '{prompt[:50]}{'...' if len(prompt)>50 else ''}':\n"
        for i, img_url in enumerate(image_urls):
            result_message += f"\nImage {i+1}: {img_url}"

        result_message += f"\n\n(Model: {chosen_model}, Size: {chosen_size})"
        if len(image_urls) > 1 :
             result_message += "\n(Note: Displaying multiple images directly in chat might be limited by platform.)"
        return result_message

    except AuthenticationError:
        return "🚫 Error: OpenAI API Key is invalid or has insufficient permissions for DALL·E. Please check your key and plan."
    except RateLimitError:
        return "🚫 Error: OpenAI API rate limit exceeded for image generation. Please try again later or check your usage."
    except APIError as e: # Catches openai.APIError, which includes BadRequestError for content policy etc.
        # print(f"OpenAI Image APIError: {e}")
        error_detail = str(e)
        if "Your request was rejected as a result of our safety system" in error_detail:
            return "🚫 Error: Your prompt was rejected by the AI's safety system. Please modify your prompt and try again."
        return f"🚫 Error: An issue occurred with the OpenAI Image API. (Status: {e.status_code if hasattr(e, 'status_code') else 'N/A'}, Message: {e.message if hasattr(e, 'message') else error_detail})"
    except Exception as e:
        # print(f"Image generation error: {e}")
        return f"🚫 Error: An unexpected error occurred while generating the image. ({e})"


if __name__ == '__main__':
    print("--- Testing AI Commands ---\n")

    print("Testing AI Ask Command (/ask):")
    # ... (ask tests remain the same) ...
    original_openai_key = get_env_variable("OPENAI_API_KEY")
    if original_openai_key and original_openai_key.startswith("sk-"):
        print(f"  Ask 'What is 2+2?':\n{get_ai_response('What is 2+2?')[:100]}...\n") # Snippet for brevity
    else:
        print("  Skipping /ask test as OPENAI_API_KEY is not set or invalid in .env.\n")
    print("-" * 20 + "\n")

    print("Testing AI Image Generation Command (/imagegen):")
    # These tests require a valid OPENAI_API_KEY with DALL·E access.
    # Simulate API key check first
    print("  --- Test Case 1: OpenAI API Key Missing/Invalid (simulated for imagegen) ---")
    if original_openai_key: # Temporarily use an invalid format for this specific test part
        os.environ["OPENAI_API_KEY"] = "INVALID_KEY_FORMAT_NO_SK"
    print(f"  Output (invalid key format): {generate_ai_image_from_prompt('A cute cat')}\n")
    if original_openai_key: # Restore it
         os.environ["OPENAI_API_KEY"] = original_openai_key
    else: # If it was never set, remove the temp invalid one
        if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"] == "INVALID_KEY_FORMAT_NO_SK":
            del os.environ["OPENAI_API_KEY"]

    print("  --- Test Case 2: No Prompt ---")
    print(f"  Output (no prompt): {generate_ai_image_from_prompt('')}\n")

    if original_openai_key and original_openai_key.startswith("sk-"):
        print("  --- Test Case 3: Valid Prompt (requires valid API key with DALL·E access in .env) ---")
        print(f"  Prompt 'A red apple on a table':\n{generate_ai_image_from_prompt('A red apple on a table', size='256x256')}\n")

        print("  --- Test Case 4: Another Valid Prompt, DALL-E 3 (if available on key) ---")
        # Note: DALL-E 3 might incur higher costs or have different availability.
        # Sticking to dall-e-2 for broader compatibility in tests unless user explicitly has dall-e-3 access.
        # print(f"  Prompt 'A futuristic cityscape at sunset, digital art' (DALL-E 3):\n{generate_ai_image_from_prompt('A futuristic cityscape at sunset, digital art', model='dall-e-3', size='1024x1024')}\n")
        print("  (Skipping DALL-E 3 test in __main__ for now to default to DALL-E 2 usage.)\n")
    else:
        print("  Skipping further OpenAI Image Generation tests as OPENAI_API_KEY is not set or invalid in .env.\n")

    print("-" * 20 + "\n")

# --- AI Text Summarization Command ---
def get_ai_summary(text_to_summarize: str = None, length_option: str = "medium") -> str:
    """
    Summarizes a given text using OpenAI's chat completion API.
    length_option can be "short", "medium", "long".
    """
    if not OPENAI_AVAILABLE:
        return "🚫 Error: The 'openai' library is not installed. Cannot use AI summarization."

    api_key = get_env_variable("OPENAI_API_KEY")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    if not api_key or not api_key.startswith("sk-"):
        return f"🚫 Error: OpenAI API key is not configured or invalid for {bot_name}.\n" \
               f"Please set a valid OPENAI_API_KEY (starting with 'sk-') in the .env file."

    if not text_to_summarize or not text_to_summarize.strip():
        return "📝 Please provide text to summarize. Usage: /summarize [short|medium|long] <your text>"

    length_instructions = {
        "short": "Provide a very concise summary, ideally 1-2 sentences or a few key bullet points.",
        "medium": "Provide a concise summary, about one paragraph or 3-5 key bullet points.",
        "long": "Provide a more detailed summary, potentially multiple paragraphs or a comprehensive list of key points, but still significantly shorter than the original."
    }

    length_guidance = length_instructions.get(length_option.lower(), length_instructions["medium"])

    system_prompt = f"You are an expert text summarizer. Your goal is to extract the key information and present it clearly. {length_guidance}"
    user_content = f"Please summarize the following text:\n\n---\n{text_to_summarize.strip()}\n---"

    try:
        client = OpenAI()

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Good balance of capability and cost for summarization
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            max_tokens=300,  # Adjust based on expected summary length, plus some buffer
            temperature=0.5  # Lower temperature for more factual, less creative summaries
        )

        summary = chat_completion.choices[0].message.content

        if not summary or not summary.strip():
            return "🤔 The AI analyzed the text but couldn't produce a summary. The text might be too short or unclear."

        return f"✍️ **Summary (Length: {length_option.capitalize()}):**\n\n{summary.strip()}"

    except AuthenticationError:
        return "🚫 Error: OpenAI API Key is invalid or has insufficient permissions. Please check your key."
    except RateLimitError:
        return "🚫 Error: OpenAI API rate limit exceeded for summarization. Please try again later."
    except APIError as e:
        # print(f"OpenAI Summarize APIError: {e}")
        return f"🚫 Error: An issue occurred with the OpenAI API during summarization. (Status: {e.status_code if hasattr(e, 'status_code') else 'N/A'}, Message: {e.message if hasattr(e, 'message') else str(e)})"
    except Exception as e:
        # print(f"Summarize command error: {e}")
        return f"🚫 Error: An unexpected error occurred while summarizing the text. ({e})"


if __name__ == '__main__':
    print("--- Testing AI Commands ---\n")

    # ... (previous AI command tests remain the same) ...
    print("Testing AI Ask Command (/ask):")
    original_openai_key = get_env_variable("OPENAI_API_KEY") # Ensure this is at the start of __main__ if other tests modify os.environ
    if original_openai_key and original_openai_key.startswith("sk-"):
        print(f"  Ask 'What is 2+2?': (result snippet)\n{get_ai_response('What is 2+2?')[:100]}...\n")
    else:
        print("  Skipping /ask test as OPENAI_API_KEY is not set or invalid in .env.\n")
    print("-" * 20 + "\n")

    print("Testing AI Image Generation Command (/imagegen):")
    # ... (imagegen tests remain the same) ...
    if original_openai_key and original_openai_key.startswith("sk-"):
         print(f"  Imagegen 'A red apple on a table' (result snippet):\n{generate_ai_image_from_prompt('A red apple on a table', size='256x256')[:150]}...\n")
    else:
        print("  Skipping /imagegen test as OPENAI_API_KEY is not set or invalid in .env.\n")
    print("-" * 20 + "\n")

    print("Testing AI Summarize Command (/summarize):")
    sample_text_short = "The quick brown fox jumps over the lazy dog. This is a classic pangram used to test typefaces."
    sample_text_long = """
    The OpenAI API provides access to powerful artificial intelligence models like GPT-3.5-turbo and GPT-4 for a variety of tasks
    including text generation, translation, summarization, and code generation. To use the API, developers need to sign up for an
    API key and can then make requests via HTTP or using official client libraries available in several programming languages such as Python.
    The API is priced based on usage, typically per token (input and output). It's important for developers to manage their API key securely
    and monitor their usage to control costs. OpenAI also enforces usage policies to prevent misuse of the technology, including generating
    harmful content. For tasks like summarization, providing clear instructions and context within the prompt can significantly improve the
    quality of the output. Different models may have different strengths, token limits, and pricing structures.
    """

    print("  --- Test Case 1: OpenAI API Key Missing/Invalid (simulated for summarize) ---")
    current_key_for_test = os.environ.get("OPENAI_API_KEY") # Save current state
    os.environ["OPENAI_API_KEY"] = "INVALID_KEY_NO_SK_PREFIX"
    print(f"  Output (invalid key format): {get_ai_summary(sample_text_short)}\n")
    if current_key_for_test is not None: # Restore
         os.environ["OPENAI_API_KEY"] = current_key_for_test
    else: # If it was never set, remove the temp invalid one
        if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"] == "INVALID_KEY_NO_SK_PREFIX":
            del os.environ["OPENAI_API_KEY"]

    print("  --- Test Case 2: No Text Provided ---")
    print(f"  Output (no text): {get_ai_summary('')}\n")

    if original_openai_key and original_openai_key.startswith("sk-"): # Use the key fetched at start of __main__
        print("  --- Test Case 3: Short Text, Medium Summary (requires valid API key) ---")
        print(f"  Summary for short text:\n{get_ai_summary(sample_text_short, length_option='medium')}\n")

        print("  --- Test Case 4: Long Text, Short Summary ---")
        print(f"  Summary for long text (short):\n{get_ai_summary(sample_text_long, length_option='short')}\n")

        print("  --- Test Case 5: Long Text, Long Summary ---")
        print(f"  Summary for long text (long):\n{get_ai_summary(sample_text_long, length_option='long')}\n")
    else:
        print("  Skipping further OpenAI Summarize tests as OPENAI_API_KEY is not set or invalid in .env.\n")

    print("-" * 20 + "\n")
