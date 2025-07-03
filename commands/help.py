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
