from utils.env_loader import get_env_variable

# According to the spec, these are the recognized prefixes.
# If setprefix is implemented, this would need to be read from a config/state.
# Now, it will receive the active prefixes as an argument.

def get_prefix_info(active_prefixes_list):
    """Generates the message displaying current bot prefixes."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    if not active_prefixes_list:
        prefix_string = "None (Commands might not be triggerable!)"
    else:
        prefix_string = " | ".join(f'"{p}"' for p in active_prefixes_list) # e.g., "/" | "." | "#"

    message = f"""
✨ {bot_name} Prefix Information ✨

{bot_name} currently responds to the following command prefixes:
{prefix_string}

For example, if "/" is an active prefix, you can use `/menu`.
Actual command triggering depends on these prefixes being checked against incoming messages.
"""
    # Note: The actual handling of multiple prefixes is not yet implemented in process_command.
    # This command only displays what the intended prefixes are as per the spec.
    return message.strip()

if __name__ == '__main__':
    # For testing the prefix command module directly
    import os
    from utils.env_loader import load_env
    # Sample active prefixes for testing
    sample_prefixes_for_test = ["/", "!", "whz"]
    if not os.path.exists(".env"):
        print("Creating dummy .env for prefix.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("BOT_NAME=TestBotPrefix\n")
    load_env()
    print(get_prefix_info(sample_prefixes_for_test))
    print("\nTesting with empty prefix list:")
    print(get_prefix_info([]))
