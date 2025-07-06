from deep_translator import GoogleTranslator
# Removed direct import of GOOGLE_LANGUAGES_TO_CODES, GOOGLE_CODES_TO_LANGUAGES
from deep_translator.exceptions import LanguageNotSupportedException, TranslationNotFound, NotValidPayload, NotValidLength
import requests # For potential network errors, though deep-translator might wrap them

# Global cache for language maps
CACHED_GOOGLE_CODES_TO_LANGUAGES = None
CACHED_GOOGLE_LANGUAGES_TO_CODES = None

def _get_google_lang_maps():
    """
    Fetches and caches Google Translate language maps from deep-translator.
    Returns (codes_to_langs_map, langs_to_codes_map).
    """
    global CACHED_GOOGLE_CODES_TO_LANGUAGES, CACHED_GOOGLE_LANGUAGES_TO_CODES
    if CACHED_GOOGLE_CODES_TO_LANGUAGES is None or CACHED_GOOGLE_LANGUAGES_TO_CODES is None:
        try:
            # This method is available on the GoogleTranslator class instance or static context in some versions
            # For deep-translator 1.11.4, it's instance method
            translator_instance_for_langs = GoogleTranslator(source='auto', target='en') # Dummy instance
            CACHED_GOOGLE_CODES_TO_LANGUAGES = translator_instance_for_langs.get_supported_languages(as_dict=True)
            if not CACHED_GOOGLE_CODES_TO_LANGUAGES: # Should not happen if library works
                 raise ValueError("Failed to fetch language map from deep-translator")
            CACHED_GOOGLE_LANGUAGES_TO_CODES = {v: k for k, v in CACHED_GOOGLE_CODES_TO_LANGUAGES.items()}
        except Exception as e:
            # print(f"Warning: Could not fetch Google language maps dynamically: {e}")
            # Provide a minimal fallback map if dynamic fetching fails
            CACHED_GOOGLE_CODES_TO_LANGUAGES = {"en": "english", "es": "spanish", "fr": "french", "de": "german", "ja": "japanese", "auto": "auto"}
            CACHED_GOOGLE_LANGUAGES_TO_CODES = {v: k for k, v in CACHED_GOOGLE_CODES_TO_LANGUAGES.items()}
    return CACHED_GOOGLE_CODES_TO_LANGUAGES, CACHED_GOOGLE_LANGUAGES_TO_CODES


DEFAULT_TARGET_LANG_CODE = "en"

def get_lang_code_from_name_or_code(lang_input: str) -> str | None:
    """
    Tries to get a valid Google Translate language code from a name or code.
    Returns the code if valid, else None. Case-insensitive for names.
    """
    if not lang_input: return None
    codes_to_langs, langs_to_codes = _get_google_lang_maps()
    lang_input_lower = lang_input.lower()
    if lang_input_lower in codes_to_langs: # It's already a code e.g. "en"
        return lang_input_lower
    if lang_input_lower in langs_to_codes: # It's a name e.g. "english"
        return langs_to_codes[lang_input_lower]
    return None

def translate_text_command(args_str: str) -> str:
    """
    Translates text based on arguments using deep-translator (GoogleTranslator).
    Format:
    1. /translate <target_lang> <text_to_translate> (source auto)
    2. /translate <source_lang> <target_lang> <text_to_translate>
    3. /translate <text_to_translate> (defaults to target_lang='en', source auto)
    Returns a string with the translation or an error message.
    """
    if not args_str or not args_str.strip():
        return "🚫 Error: No text or arguments provided for translation. \n" \
               "Usage: /translate [source_lang] <target_lang> <text> OR /translate <text> (to English)"

    parts = args_str.strip().split()

    text_to_translate_list = []
    source_lang_code = 'auto'
    target_lang_code = DEFAULT_TARGET_LANG_CODE

    # Argument parsing logic
    if len(parts) >= 1:
        # Try to parse up to two language codes from the beginning
        lang1_candidate = get_lang_code_from_name_or_code(parts[0])
        lang2_candidate = None
        if len(parts) >= 2:
            lang2_candidate = get_lang_code_from_name_or_code(parts[1])

        if lang1_candidate and lang2_candidate and len(parts) > 2:
            # Case: <source_lang> <target_lang> <text...>
            source_lang_code = lang1_candidate
            target_lang_code = lang2_candidate
            text_to_translate_list = parts[2:]
        elif lang1_candidate and len(parts) > 1:
            # Case: <target_lang> <text...> (source will be 'auto')
            target_lang_code = lang1_candidate
            text_to_translate_list = parts[1:]
        else:
            # Case: <text_to_translate> (all parts are text)
            text_to_translate_list = parts
            # source_lang_code remains 'auto', target_lang_code remains DEFAULT_TARGET_LANG_CODE

    if not text_to_translate_list:
         return "🚫 Error: No text provided for translation after parsing arguments."

    text_to_translate = " ".join(text_to_translate_list)

    # Validate final language codes (target must be specific, source can be auto)
    if target_lang_code == 'auto': # Target cannot be auto
        return "🚫 Error: Target language cannot be 'auto'. Please specify a target language."
    if get_lang_code_from_name_or_code(target_lang_code) is None: # Check if target is valid
        return f"🚫 Error: Invalid target language: '{target_lang_code}'. Use codes like 'en', 'es', 'fr' or full names."
    if source_lang_code != 'auto' and get_lang_code_from_name_or_code(source_lang_code) is None:
        return f"🚫 Error: Invalid source language: '{source_lang_code}'. Use codes, full names, or 'auto'."

    try:
        # deep-translator's GoogleTranslator can detect source if source='auto'
        translator_instance = GoogleTranslator(source=source_lang_code, target=target_lang_code)
        translated_text = translator_instance.translate(text_to_translate)

        # For display, try to determine the actual source language if 'auto' was used
        actual_source_lang_code_for_display = source_lang_code
        if source_lang_code == 'auto':
            try:
                # Some translators in deep-translator provide detected source, GoogleTranslator does not directly.
                # We can try a separate detection call, or rely on user knowing what they typed.
                # For simplicity, if source was 'auto', we can say "auto-detected".
                # A more robust way if translator_instance had a .detected_source_language attribute.
                # Let's assume for now if 'auto', we can't reliably show what it detected without another call.
                # The library might handle this internally and just translate.
                # For a better user experience, we might want to make a separate detect call:
                if len(text_to_translate) > 1: # Avoid detection on very short strings
                    detected = GoogleTranslator().detect(text_to_translate[:100]) # Detect on a sample
                    if detected and detected[0]:
                        actual_source_lang_code_for_display = detected[0][0]
            except Exception:
                 actual_source_lang_code_for_display = "auto-detected" # Fallback

        if translated_text is None:
            return f"😕 Could not translate '{text_to_translate[:30]}...'. The translation result was empty."

        codes_to_langs, _ = _get_google_lang_maps() # Fetch maps for display names
        source_display_name = codes_to_langs.get(actual_source_lang_code_for_display, actual_source_lang_code_for_display).capitalize()
        target_display_name = codes_to_langs.get(target_lang_code, target_lang_code).capitalize()

        return f"🌍 Translation ({source_display_name} -> {target_display_name}):\n" \
               f"-------------------------------------\n" \
               f"{translated_text}\n" \
               f"-------------------------------------"

    except LanguageNotSupportedException as lns_err:
        return f"🚫 Error: Language not supported by the translation service. Details: {lns_err}"
    except TranslationNotFound as tnf_err:
        return f"🚫 Error: Translation not found for the given text (the text might be too short or untranslatable). Details: {tnf_err}"
    except NotValidPayload as nvp_err:
        return f"🚫 Error: The text provided for translation is not valid (e.g. too long, or empty after processing). Details: {nvp_err}"
    except NotValidLength as nvl_err:
        return f"🚫 Error: The text provided is too long to be translated by this service. Details: {nvl_err}"
    except requests.exceptions.RequestException as net_err: # Catch network errors from requests used by deep-translator
        return f"🚫 Error: Network problem while connecting to translation service. ({net_err})"
    except Exception as e:
        # print(f"Deep Translation error: {type(e).__name__}: {e}") # For logging
        return f"🚫 Error: Could not translate text due to an unexpected issue. ({type(e).__name__})"

if __name__ == '__main__':
    print("Testing translation function (with deep-translator):\n")

    test_cases_deep_translator = [
        "es Hello world",                     # Target lang, text
        "auto es Hello world from English",   # Explicit auto source, target, text
        "Hola mundo",                         # Text only (to English by default logic)
        "ja こんにちは世界",                  # Japanese text (to English by default logic)
        "en de Hallo Welt",                   # English to German
        "German Guten Tag",                   # Target lang (name), text
        "French Spanish Bonjour le monde",    # Source lang (name), target lang (name), text
        "zz This should fail with lang",      # Invalid target lang code (zz)
        "en zz This should also fail",        # Invalid target lang code (zz)
        "",                                   # Empty input
        "es",                                 # Lang code only, no text
        "english french This is a test to translate from English to French.",
        "This is a test sentence to translate into Spanish from English just for fun." # Text only, longer
    ]

    for i, case_str in enumerate(test_cases_deep_translator):
        print(f"Input {i+1}: '/translate {case_str}'")
        result = translate_text_command(case_str)
        print(f"  Output:\n{result}\n")

    print(f"Input: '/translate fr de Bonjour le monde'") # fr de text
    print(f"  Output:\n{translate_text_command('fr de Bonjour le monde')}\n")

    print(f"Input: '/translate de fr Guten Tag'") # de fr text
    print(f"  Output:\n{translate_text_command('de fr Guten Tag')}\n")
