from utils.env_loader import get_env_variable

# This list will be updated as more commands are added.
# For a truly dynamic help, we might inspect the commands directory or use a registration pattern.
# For now, a manually curated list is fine as per the plan.
COMMANDS_LIST = {
    "/ping": "Checks bot's responsiveness and uptime.",
    "/menu": "Displays the main interactive menu.",
    "/stats": "Shows system CPU, memory, and OS statistics.",
    "/about": "Provides information about the bot.",
    "/support": "Shows the link to the official support group.",
    "/prefix": "Displays the current command prefixes.",
    "/setprefix <prefixes>": "Sets new command prefixes (e.g., /setprefix ! $).",
    "/report": "Shows instructions on how to report bugs or issues.",
    "/invite": "Shows information on how to invite the bot or share it.",
    "/calc <expression>": "Calculates a mathematical expression (e.g., /calc 2+2*5).",
    "/qr <text>": "Generates a QR code from the provided text.",
    "/translate [src] <tgt> <text>": "Translates text. E.g.: /translate es hello world",
    "/shorturl <url>": "Shortens a long URL using TinyURL.",
    "/weather <location>": "Fetches current weather for a location (e.g., /weather London).",
    "/time [timezone]": "Shows current time. E.g., /time Europe/London or /time for server local.",
    "/dictionary <word>": "Gets definitions for an English word.",
    "/quote": "Fetches a random inspirational quote.",
    "/coinflip": "Flips a virtual coin (Heads or Tails).",
    "/8ball <question>": "Asks the Magic 8-Ball a yes/no question.",
    "/rate [item]": "Rates the specified item (or your vibe) out of 100.",
    "/rps <choice>": "Play Rock, Paper, Scissors (e.g., /rps rock).",
    "/truth": "Gives you a random truth question.",
    "/dare": "Gives you a random dare challenge.",
    "/ship <name1> [name2]": "Calculates love compatibility between names.",
    "/guess <number>": "Guess a number (1-10). Bot tells you if you're right!",
    "/reverse <text>": "Reverses the provided text.",
    "/fancy [style] <text>": "Converts text to fancy Unicode. Styles: bold_serif, script, fraktur, cursive.",
    "/zalgo [intensity] <text>": "Converts text to Zalgo (glitch) text. Intensities: low, normal, high, max.",
    "/tinytext <text>": "Converts text to tiny Unicode (small caps).",
    "/ascii [font] <text>": "Generates ASCII art from text. Fonts: standard, slant, big, etc.",
    "/emoji <keyword>": "Finds emojis related to a keyword (e.g., /emoji happy).",
    "/base64 <encode|decode> <string>": "Encodes or decodes a string using Base64.",
    "/jsonfmt <json_string>": "Formats (pretty-prints) a JSON string.",
    "/whois <domain_name>": "Performs a WHOIS lookup for a domain name.",
    "/help": "Shows this help message with all available commands."
    # Add new commands here as they are implemented
}

def get_help_message():
    """Generates a formatted help message listing all available commands."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    help_text = f"🌟 Welcome to {bot_name}! Here are the available commands: 🌟\n\n"

    if not COMMANDS_LIST:
        help_text += "No commands are currently available."
        return help_text

    # Determine the maximum command length for alignment
    max_cmd_len = 0
    if COMMANDS_LIST: # Check if COMMANDS_LIST is not empty
        max_cmd_len = max(len(cmd) for cmd in COMMANDS_LIST)

    for command, description in COMMANDS_LIST.items():
        # Simple padding for alignment.
        # A more sophisticated table format could be used if needed.
        padding = " " * (max_cmd_len - len(command))
        help_text += f"🔹 {command}{padding}  : {description}\n"

    help_text += f"\nType a command to get started, e.g., /ping."
    help_text += f"\nFor the main menu, type /menu."

    # Could add prefix info here later if it becomes dynamic
    # current_prefix = get_env_variable("PREFIX", "/")
    # help_text += f"\nCurrent command prefix is: {current_prefix}"


    return help_text.strip()

if __name__ == '__main__':
    # For testing the help message generation directly
    import os
    from utils.env_loader import load_env
    if not os.path.exists(".env"):
        print("Creating dummy .env for help.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("OWNER_NAME=TestOwnerHelp\n")
            f.write("BOT_NAME=TestBotHelp\n")
    load_env() # Load .env for BOT_NAME
    print(get_help_message())
