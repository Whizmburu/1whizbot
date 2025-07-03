from utils.env_loader import get_env_variable

# According to the spec, these are the recognized prefixes.
# This will be hardcoded for now for the display command.
# If setprefix is implemented, this would need to be read from a config/state.
CURRENT_PREFIXES = ["/", ".", "#", "whz", "!"]

def get_prefix_info():
    """Generates the message displaying current bot prefixes."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    prefix_string = " | ".join(f'"{p}"' for p in CURRENT_PREFIXES) # e.g., "/" | "." | "#"

    message = f"""
✨ {bot_name} Prefix Information ✨

{bot_name} currently responds to the following command prefixes:
{prefix_string}

For example, you can use `/menu` or `.menu` (if those prefixes are active and handled).
The primary prefix is usually `/`.
"""
    # Note: The actual handling of multiple prefixes is not yet implemented in process_command.
    # This command only displays what the intended prefixes are as per the spec.
    return message.strip()

if __name__ == '__main__':
    # For testing the prefix command module directly
    import os
    from utils.env_loader import load_env
    if not os.path.exists(".env"):
        print("Creating dummy .env for prefix.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("BOT_NAME=TestBotPrefix\n")
    load_env()
    print(get_prefix_info())
