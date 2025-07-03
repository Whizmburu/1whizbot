import requests

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def get_word_definition(word: str) -> str:
    """
    Fetches definitions for a given English word using dictionaryapi.dev.
    Returns a formatted string with definitions or an error message.
    """
    if not word or not word.strip():
        return "🚫 Error: No word provided. Usage: /dictionary <word>"

    word_to_lookup = word.strip().lower() # API is generally case-insensitive but good practice

    try:
        response = requests.get(f"{API_URL}{word_to_lookup}", timeout=10)

        # Check if the word was not found (API returns 404)
        if response.status_code == 404:
            return f"😕 Word not found: '{word}'. Please check the spelling or try another word."

        response.raise_for_status() # Raise HTTPError for other bad responses (4XX or 5XX)

        data = response.json() # This will be a list of entries

        if not data or not isinstance(data, list):
            # Should be caught by 404 or other HTTP errors, but as a safeguard
            return f"😕 No definition data found for '{word}'."

        # Formatting the output
        # A word can have multiple entries (e.g. noun, verb) and multiple meanings per entry.
        output_parts = [f"📖 Definitions for \"{data[0].get('word', word_to_lookup)}\":"]

        phonetic_text = data[0].get('phonetic') # Overall phonetic if available
        if phonetic_text:
            output_parts.append(f"   🗣️ Phonetic: {phonetic_text}")

        # Iterate through each entry (usually one, but API can return multiple for homographs)
        for entry_index, entry_data in enumerate(data):
            if entry_index > 0 : # If there's more than one entry block (rare for this API for simple words)
                output_parts.append(f"\n--- Entry {entry_index + 1} for \"{entry_data.get('word', word_to_lookup)}\" ---")
                entry_phonetic = entry_data.get('phonetic')
                if entry_phonetic:
                    output_parts.append(f"   🗣️ Phonetic: {entry_phonetic}")


            # Phonetics specific to this entry (if different or more detailed)
            # Sometimes phonetics are in a list
            phonetics_list = entry_data.get('phonetics', [])
            if not phonetic_text and phonetics_list: # If no overall phonetic, use first from list
                for ph in phonetics_list:
                    if ph.get('text'):
                        output_parts.append(f"   🗣️ Phonetic: {ph.get('text')}")
                        if ph.get('audio'):
                             output_parts.append(f"      (Audio: {ph.get('audio')})") # API provides audio links
                        break # Take the first one with text

            # Meanings (part of speech, definitions, examples)
            for meaning_index, meaning in enumerate(entry_data.get('meanings', [])):
                part_of_speech = meaning.get('partOfSpeech', 'N/A').capitalize()
                output_parts.append(f"\n🔹 As {part_of_speech}:")

                for def_index, definition_obj in enumerate(meaning.get('definitions', [])):
                    definition_text = definition_obj.get('definition', 'No definition text.')
                    output_parts.append(f"  {def_index + 1}. {definition_text}")

                    example = definition_obj.get('example')
                    if example:
                        output_parts.append(f"     Example: \"{example}\"")

                    synonyms = definition_obj.get('synonyms')
                    if synonyms:
                         output_parts.append(f"     Synonyms: {', '.join(synonyms[:3])}{'...' if len(synonyms) > 3 else ''}") # Show a few

                    # Limit to a few definitions per part of speech to avoid spam
                    if def_index >= 2 and meaning_index < len(entry_data.get('meanings', []))-1 : # Show max 3 defs unless it's the last PoS
                        output_parts.append("     (more definitions exist...)")
                        break
            if entry_index >=1: # Limit to 2 full entries from API response
                 output_parts.append("\n(More entries might exist if word has multiple distinct forms)")
                 break


        return "\n".join(output_parts)

    except requests.exceptions.HTTPError as http_err:
        # print(f"Dictionary API HTTP error: {http_err} - {response.text if 'response' in locals() else 'N/A'}")
        return f"🚫 Error: Could not fetch definition. HTTP {response.status_code if 'response' in locals() else 'Unknown'}."
    except requests.exceptions.RequestException as req_err:
        # print(f"Dictionary API Request error: {req_err}")
        return "🚫 Error: Network problem or could not connect to the dictionary service."
    except Exception as e:
        # print(f"Dictionary command error: {e}")
        return f"🚫 Error: An unexpected error occurred while fetching definition. ({e})"

if __name__ == '__main__':
    print("Testing Dictionary Command:\n")

    test_words = [
        "hello",
        "programming",
        "lexicon",
        "ubiquitous",
        "nonexistentwordxyz", # Word not found
        "", # Empty input
        "  bank  " # Word with whitespace
    ]

    for i, word_str in enumerate(test_words):
        print(f"Input {i+1}: '{word_str}'")
        result = get_word_definition(word_str)
        print(f"  Output:\n{result}\n")
        print("---------------------------------------\n")

    # Test a word with multiple meanings / parts of speech
    print("Input: 'set'")
    result_set = get_word_definition("set")
    print(f"  Output for 'set':\n{result_set}\n")
    print("---------------------------------------\n")

    print("Input: 'run'")
    result_run = get_word_definition("run")
    print(f"  Output for 'run':\n{result_run}\n")
    print("---------------------------------------\n")
