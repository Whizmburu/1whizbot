from googletrans import Translator, LANGUAGES

# Pre-create a translator instance
translator = Translator()

DEFAULT_TARGET_LANG = "en"

def get_language_name(lang_code):
    """Returns the full name of a language from its code, or the code itself if not found."""
    return LANGUAGES.get(lang_code.lower(), lang_code)

def translate_text_command(args_str: str) -> str:
    """
    Translates text based on arguments.
    Format:
    1. /translate <target_lang> <text_to_translate>
    2. /translate <source_lang> <target_lang> <text_to_translate>
    3. /translate <text_to_translate> (defaults to target_lang='en')
    Returns a string with the translation or an error message.
    """
    if not args_str or not args_str.strip():
        return "🚫 Error: No text or arguments provided for translation. \n" \
               "Usage: /translate [source_lang] <target_lang> <text> OR /translate <text> (to English)"

    parts = args_str.strip().split()

    text_to_translate_list = []
    source_lang = None
    target_lang = None

    # Try to parse language codes
    # Scenario 1: Only text provided (translate to default English)
    if len(parts) == 1 and parts[0].lower() not in LANGUAGES and len(parts[0]) > 2 : # Heuristic: single word not a lang code and longer than 2 chars
        text_to_translate_list = parts
        target_lang = DEFAULT_TARGET_LANG
        source_lang = 'auto' # Auto-detect source
    elif len(parts) >= 2:
        # Scenario 2: <target_lang> <text>
        # Check if first part is a valid lang code
        if parts[0].lower() in LANGUAGES or parts[0].lower() in LANGUAGES.values():
            target_lang_candidate = parts[0].lower()
            # If it's a language name, convert to code
            if target_lang_candidate in LANGUAGES.values():
                target_lang_candidate = [code for code, name in LANGUAGES.items() if name == target_lang_candidate][0]

            # Check if second part is also a lang code (for src_lang target_lang text)
            if len(parts) >= 3 and (parts[1].lower() in LANGUAGES or parts[1].lower() in LANGUAGES.values()):
                source_lang_candidate = target_lang_candidate # First part was source
                target_lang_candidate = parts[1].lower()
                if target_lang_candidate in LANGUAGES.values(): # Convert name to code
                     target_lang_candidate = [code for code, name in LANGUAGES.items() if name == target_lang_candidate][0]

                if source_lang_candidate not in LANGUAGES:
                    return f"🚫 Error: Invalid source language code/name: '{parts[0]}'."
                if target_lang_candidate not in LANGUAGES:
                    return f"🚫 Error: Invalid target language code/name: '{parts[1]}'."

                source_lang = source_lang_candidate
                target_lang = target_lang_candidate
                text_to_translate_list = parts[2:]
            else: # First part was target_lang, source is auto
                if target_lang_candidate not in LANGUAGES:
                     return f"🚫 Error: Invalid target language code/name: '{parts[0]}'."
                target_lang = target_lang_candidate
                source_lang = 'auto'
                text_to_translate_list = parts[1:]
        else: # No lang codes at the start, assume all is text, translate to default
            text_to_translate_list = parts
            target_lang = DEFAULT_TARGET_LANG
            source_lang = 'auto'
    else: # Not enough parts for any valid structure with lang codes, assume all is text
        text_to_translate_list = parts
        target_lang = DEFAULT_TARGET_LANG
        source_lang = 'auto'

    if not text_to_translate_list:
        return "🚫 Error: No text provided for translation after parsing arguments."

    text_to_translate = " ".join(text_to_translate_list)

    if target_lang is None: # Should have been set by now, but as a fallback
        target_lang = DEFAULT_TARGET_LANG
    if source_lang is None:
        source_lang = 'auto'

    try:
        # Perform translation
        translated_obj = translator.translate(text_to_translate, dest=target_lang, src=source_lang)

        detected_src_lang_code = translated_obj.src
        detected_src_lang_name = get_language_name(detected_src_lang_code)
        target_lang_name = get_language_name(target_lang)

        return f"🌍 Translation ({detected_src_lang_name} -> {target_lang_name}):\n" \
               f"-------------------------------------\n" \
               f"{translated_obj.text}\n" \
               f"-------------------------------------"

    except Exception as e:
        # print(f"Translation error: {e}") # For logging
        if "invalid destination language" in str(e).lower():
            return f"🚫 Error: Invalid target language specified: '{target_lang}'. Please use a valid language code (e.g., 'en', 'es', 'fr')."
        return f"🚫 Error: Could not translate text. ({e})"

if __name__ == '__main__':
    test_cases = [
        "es Hello world",                     # Target lang, text
        "fr en Hello world from English",     # Source, target, text
        "Hola mundo",                         # Text only (to English)
        "ja こんにちは世界",                  # Japanese text (to English)
        "auto de Hallo Welt",                 # Auto source, target German
        "en es Hello world",                  # English to Spanish
        "Spanish Hola mundo",                 # Target lang (name), text
        "English Spanish Hello world",        # Source lang (name), target lang (name), text
        "zz This should fail",                # Invalid target lang code
        "en zz This should also fail",        # Invalid target lang code
        "",                                   # Empty input
        "es",                                 # Lang code only, no text
        "This is a test sentence to translate into Spanish from English just for fun.", # Longer text to default
        "fr de Bonjour le monde",             # French to German
        "de fr Guten Tag",                    # German to French
    ]

    print("Testing translation function:\n")
    for i, case_str in enumerate(test_cases):
        print(f"Input {i+1}: '/translate {case_str}'")
        result = translate_text_command(case_str)
        print(f"  Output: {result}\n")

    print("Test with only text (long):")
    only_text_case = "Ceci est une phrase en français à traduire automatiquement en anglais."
    print(f"Input: '/translate {only_text_case}'")
    result_only_text = translate_text_command(only_text_case)
    print(f"  Output: {result_only_text}\n")

    print("Test with only target language (full name) and text:")
    target_name_case = "German Hello world, how are you?"
    print(f"Input: '/translate {target_name_case}'")
    result_target_name = translate_text_command(target_name_case)
    print(f"  Output: {result_target_name}\n")

    print("Test with only source language (full name), target (code) and text:")
    source_name_case = "French es Bonjour, comment ça va?"
    print(f"Input: '/translate {source_name_case}'")
    result_source_name = translate_text_command(source_name_case)
    print(f"  Output: {result_source_name}\n")
