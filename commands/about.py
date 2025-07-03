from utils.env_loader import get_env_variable

def get_about_info():
    """Generates the bot's about information string."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
    owner_name = get_env_variable("OWNER_NAME", "WHIZ")
    version = "v1.0.0" # Hardcoded for now
    repo_url = "github.com/WHIZ-MD/Bot"
    description = f"{bot_name} is a versatile WhatsApp assistant, designed to bring a wide array of functionalities to your chats. Developed by {owner_name}."

    about_message = f"""
╔═══════[ 🌟 ABOUT {bot_name} 🌟 ]═══════╗
║ 🤖 Name        : {bot_name}
║ 👑 Owner       : {owner_name}
║ 📝 Description : {description}
║ ℹ️ Version     : {version}
║ 🔗 Repository  : {repo_url}
║
║ Type /help to see all available commands.
╚═══════════════════════════════════╝
"""
    # A more dynamic description could be nice later
    # For example, description = get_env_variable("BOT_DESCRIPTION", "A helpful WhatsApp bot.")

    return about_message.strip()

if __name__ == '__main__':
    # For testing the about command module directly
    # Need to ensure .env is loaded for get_env_variable
    import os
    from utils.env_loader import load_env
    if not os.path.exists(".env"):
        print("Creating dummy .env for about.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("OWNER_NAME=TestOwnerAbout\n")
            f.write("BOT_NAME=TestBotAbout\n")
    load_env()
    print(get_about_info())
    # Clean up dummy .env if it was created by this test
    # if "TestOwnerAbout" in open(".env").read():
        # os.remove(".env")
        # Let's not auto-remove, might interfere with other tests or actual .env
    pass
