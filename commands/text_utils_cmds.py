import random # Will be needed for other text utils like Zalgo

# --- Reverse Text Command ---
def reverse_text(text_to_reverse: str = None) -> str:
    """
    Reverses the given string.
    """
    if not text_to_reverse or not text_to_reverse.strip():
        return "🔄 Please provide some text to reverse! Usage: /reverse <your text>"

    reversed_str = text_to_reverse.strip()[::-1]
    return f"🔁 Reversed text: \"{reversed_str}\""

# --- Fancy Text Command ---

# Define character maps for different styles
# Using mathematical alphanumeric symbols: https://en.wikipedia.org/wiki/Mathematical_Alphanumeric_Symbols
FANCY_STYLES = {
    "bold_serif": {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌',
        'N': '𝐍', 'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦',
        'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    },
    "script": { # Mathematical Script
        'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢', 'H': 'ℋ', 'I': 'ℐ', 'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ',
        'N': '𝒩', 'O': '𝒪', 'P': '𝒫', 'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰', 'V': '𝒱', 'W': '𝒲', 'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵',
        'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': 'ℯ', 'f': '𝒻', 'g': 'ℊ', 'h': '𝒽', 'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂',
        'n': '𝓃', 'o': 'ℴ', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊', 'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏',
        # Numbers are not typically available in script style directly, so they'll pass through
    },
    "fraktur": { # Mathematical Fraktur
        'A': '𝔄', 'B': '𝔅', 'C': 'ℭ', 'D': '𝔇', 'E': '𝔈', 'F': '𝔉', 'G': '𝔊', 'H': 'ℌ', 'I': 'ℑ', 'J': '𝔍', 'K': '𝔎', 'L': '𝔏', 'M': '𝔐',
        'N': '𝔑', 'O': '𝔒', 'P': '𝔓', 'Q': '𝔔', 'R': 'ℜ', 'S': '𝔖', 'T': '𝔗', 'U': '𝔘', 'V': '𝔙', 'W': '𝔚', 'X': '𝔛', 'Y': '𝔜', 'Z': 'ℨ',
        'a': '𝔞', 'b': '𝔟', 'c': '𝔠', 'd': '𝔡', 'e': '𝔢', 'f': '𝔣', 'g': '𝔤', 'h': '𝔥', 'i': '𝔦', 'j': '𝔧', 'k': '𝔨', 'l': '𝔩', 'm': '𝔪',
        'n': '𝔫', 'o': '𝔬', 'p': '𝔭', 'q': '𝔮', 'r': '𝔯', 's': '𝔰', 't': '𝔱', 'u': '𝔲', 'v': '𝔳', 'w': '𝔴', 'x': '𝔵', 'y': '𝔶', 'z': '𝔷',
    }
    # Add more styles (e.g., monospace, double-struck) here as needed
}
DEFAULT_FANCY_STYLE = "bold_serif"

def generate_fancy_text(text_to_fancy: str, style_choice: str = None) -> str:
    """
    Converts plain text to a fancy Unicode text style.
    """
    if not text_to_fancy or not text_to_fancy.strip():
        return "💅 Please provide some text to make fancy! Usage: /fancy [style] <your text>"

    text_to_fancy = text_to_fancy.strip()

    chosen_style_key = DEFAULT_FANCY_STYLE
    if style_choice and style_choice.strip().lower() in FANCY_STYLES:
        chosen_style_key = style_choice.strip().lower()
    elif style_choice: # User specified a style but it's not found
        available_styles = ", ".join(FANCY_STYLES.keys())
        return f"💅 Style '{style_choice}' not found. Available styles: {available_styles}. Using default '{DEFAULT_FANCY_STYLE}'."
        # Or just proceed with default without error message, and the original text_to_fancy is used.

    char_map = FANCY_STYLES.get(chosen_style_key, {})

    fancified_text = ""
    converted_chars = 0
    for char in text_to_fancy:
        fancy_char = char_map.get(char)
        if fancy_char:
            fancified_text += fancy_char
            converted_chars +=1
        else:
            fancified_text += char # Keep original character if no mapping

    if converted_chars == 0 and chosen_style_key != DEFAULT_FANCY_STYLE and style_choice : # User chose a specific style but no chars were converted
         return f"💅 Could not convert '{text_to_fancy}' to style '{chosen_style_key}'. This style might not support these characters."


    return f"✨ Fancy ({chosen_style_key}): {fancified_text}"

# --- Zalgo Text Command ---
# Unicode combining diacritical marks
# Selected a small subset for simplicity. More can be added.
# See: https://en.wikipedia.org/wiki/Combining_Diacritical_Marks
ZALGO_UP = [
    '\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310',
    '\u0352', '\u0357', '\u0351', '\u0307', '\u0308', '\u030a', '\u0342', '\u0343',
    '\u0344', '\u034a', '\u034b', '\u034c', '\u0303', '\u0302', '\u030c', '\u0350'
]
ZALGO_DOWN = [
    '\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e', '\u031f',
    '\u0320', '\u0324', '\u0325', '\u0326', '\u0329', '\u032a', '\u032b', '\u032c',
    '\u032d', '\u032e', '\u032f', '\u0330', '\u0331', '\u0332', '\u0333', '\u0339'
]
ZALGO_MID = [
    '\u0315', '\u031b', '\u0340', '\u0341', '\u0358', '\u0323', '\u0334', '\u0335',
    '\u0336', '\u034f', '\u035c', '\u035d', '\u035e', '\u035f', '\u0360', '\u0361',
    '\u0362', '\u0338', '\u0337', '\u0362', '\u0489'
]

def generate_zalgo_text(text_to_zalgo: str, intensity: str = "normal") -> str:
    """
    Converts plain text to Zalgo text by adding combining diacritical marks.
    Intensity can be 'low', 'normal', 'high'.
    """
    if not text_to_zalgo or not text_to_zalgo.strip():
        return "☣️ Please provide some text to Zalgo-fy! Usage: /zalgo [intensity] <text>"

    text_to_zalgo = text_to_zalgo.strip()

    intensity_map = {
        "low": (1, 2), # Min/max diacritics per original char section (up/mid/down)
        "normal": (2, 4),
        "high": (4, 8),
        "max": (8, 16) # Very intense
    }

    min_dia, max_dia = intensity_map.get(intensity.lower(), intensity_map["normal"])

    zalgo_fied_text = ""
    for char in text_to_zalgo:
        zalgo_fied_text += char
        # Add 'up' diacritics
        for _ in range(random.randint(min_dia // 2, max_dia // 2)): # Fewer up usually looks better
            if ZALGO_UP: zalgo_fied_text += random.choice(ZALGO_UP)
        # Add 'mid' diacritics
        for _ in range(random.randint(min_dia, max_dia)):
            if ZALGO_MID: zalgo_fied_text += random.choice(ZALGO_MID)
        # Add 'down' diacritics
        for _ in range(random.randint(min_dia, max_dia)):
            if ZALGO_DOWN: zalgo_fied_text += random.choice(ZALGO_DOWN)

    return f"👻 Zalgo: {zalgo_fied_text}"

# --- Tiny Text (Small Caps) Command ---
# Primarily for a-z. Some other characters might have small cap forms, but this is a basic set.
# Full list of small caps: https://en.wikipedia.org/wiki/Small_caps#Unicode
# Using Unicode Small Capitals from the IPA Extensions block and Phonetic Extensions block mostly.
TINY_TEXT_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
    'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ꞯ', # Note: q is often tricky or missing a standard small cap
    'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
    # Uppercase to small caps (some are same as lowercase small caps, some distinct if available)
    'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ', 'H': 'ʜ', 'I': 'ɪ',
    'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ꞯ',
    'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ',
    # Numbers (not standard small caps, but some "petite" forms exist, or just pass through)
    # For simplicity, numbers will pass through.
}
# Note: True small caps for 'Q', 'S', 'X' are often problematic or look like lowercase.
# The map above uses what's commonly available and visually distinct where possible.
# 'q' uses U+A7AF (Latin Letter Small Capital Q)
# 's' and 'x' often just use their lowercase forms as small caps if no dedicated char is widely supported or visually distinct.

def generate_tiny_text(text_to_tiny: str) -> str:
    """
    Converts text to a "tiny text" representation using Unicode small capital letters.
    """
    if not text_to_tiny or not text_to_tiny.strip():
        return "ˢᵐᵃˡˡ Please provide some text to make tiny! Usage: /tinytext <your text>"

    text_to_tiny = text_to_tiny.strip() # No need to lower, map handles both cases if defined

    tinified_text = ""
    for char in text_to_tiny:
        tinified_text += TINY_TEXT_MAP.get(char, char) # Keep original if no mapping

    return f"🤏 Tiny Text: {tinified_text}"


if __name__ == '__main__':
    print("--- Testing Text Utils Commands ---\n")

    print("Testing Reverse Text:")
    print(f"  Input 'hello world': {reverse_text('hello world')}")
    print(f"  Input '  madam  ': {reverse_text('  madam  ')}") # Palindrome test with spaces
    print(f"  Input '12345': {reverse_text('12345')}")
    print(f"  Input (empty): {reverse_text('')}")
    print(f"  Input (None): {reverse_text(None)}")
    print(f"  Input (special chars !@#): {reverse_text('!@# test #@!')}")
    print("-" * 20 + "\n")

    print("Testing Fancy Text:")
    print(f"  Default style ('Hello 123'): {generate_fancy_text('Hello 123')}")
    print(f"  Bold Serif ('Bold Test 456'): {generate_fancy_text('Bold Test 456', 'bold_serif')}")
    print(f"  Script ('Script Test 789'): {generate_fancy_text('Script Test 789', 'script')}")
    print(f"  Fraktur ('Fraktur Test 000'): {generate_fancy_text('Fraktur Test 000', 'fraktur')}")
    print(f"  Invalid style ('unknownstyle Test'): {generate_fancy_text('Unknown Style Test', 'unknownstyle')}")
    print(f"  No text: {generate_fancy_text('')}")
    print(f"  No text with style: {generate_fancy_text(None, 'script')}")
    print(f"  Special chars (should pass through): {generate_fancy_text('Hello @ World!', 'script')}")
    print(f"  Script style with numbers (should pass numbers): {generate_fancy_text('Test 123 Go', 'script')}")
    print("-" * 20 + "\n")

    print("Testing Zalgo Text:")
    print(f"  No text: {generate_zalgo_text('')}")
    print(f"  'Zalgo Test' (default intensity): {generate_zalgo_text('Zalgo Test')}")
    print(f"  'Low Intensity' (low): {generate_zalgo_text('Low Intensity', 'low')}")
    print(f"  'High Intensity' (high): {generate_zalgo_text('High Intensity', 'high')}")
    print(f"  'Max Intensity' (max): {generate_zalgo_text('Max Intensity', 'max')}")
    print(f"  'Invalid Intensity' (invalid): {generate_zalgo_text('Invalid Intensity', 'superhigh')}") # Should use normal
    print("-" * 20 + "\n")

    print("Testing Tiny Text:")
    print(f"  No text: {generate_tiny_text('')}")
    print(f"  'Hello World 123': {generate_tiny_text('Hello World 123')}")
    print(f"  'abcdefghijklmnopqrstuvwxyz': {generate_tiny_text('abcdefghijklmnopqrstuvwxyz')}")
    print(f"  'ABCDEFGHIJKLMNOPQRSTUVWXYZ': {generate_tiny_text('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}")
    print(f"  'Special @ Chars !': {generate_tiny_text('Special @ Chars !')}")
    print("-" * 20 + "\n")
