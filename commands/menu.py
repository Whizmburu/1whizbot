from utils.uptime import get_uptime
from utils.env_loader import get_env_variable

def get_menu_text():
    """Generates the main menu text."""

    owner_name = get_env_variable("OWNER_NAME", "WHIZ")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
    repo_link = "github.com/WHIZ-MD/Bot" # Hardcoded as per spec
    current_prefix = "/" # Hardcoded for now, can be made dynamic later
    forks_count = 327 # Hardcoded as per spec
    command_count = 85 # Hardcoded as per spec, will be dynamic later
    uptime_str = get_uptime()
    support_group_link = "https://chat.whatsapp.com/JLmSbTfqf4I2Kh4SNJcWgM" # Hardcoded
    logo_url = "https://i.ibb.co/sp1hFpKj/whizmd.png" # Hardcoded

    menu = f"""
<div style="text-align:center; margin-bottom: 15px;">
  <a href="{support_group_link}" target="_blank">
    <img src="{logo_url}" alt="{bot_name} Bot Logo" width="180" style="border-radius: 20px; box-shadow: 0 0 10px #00ffcc;">
  </a>
</div>

╔════[ 🌺 {bot_name} MENU 🌺 ]════╗
║ 👑 Owner     : {owner_name}
║ 📁 Repo      : {repo_link}
║ 🔤 Prefix    : "{current_prefix}" | "." | "#" | "whz" | "!"
║ 🍜 Forks     : {forks_count}
║ 🔹 Commands  : {command_count}
║ ⏱ Uptime    : {uptime_str}
║
║ 🔹 Use /help or /menu to explore more
║ 📞 Support Group:
║      📣 <click the {bot_name} logo above/below or link>
║      {support_group_link}
╚══════════════════════════════════╝
"""
    # The HTML part will render as text in console.
    # For WhatsApp, this would need to be sent as part of a rich message if supported,
    # or the image could be sent separately with the text.
    # The spec shows the logo embedded, which implies a capability beyond plain text.
    # For now, we include the HTML structure as requested.

    return menu.strip()

if __name__ == '__main__':
    # For testing the menu display directly
    # Need to ensure .env is loaded if this is run standalone for get_env_variable to work
    import os
    from utils.env_loader import load_env
    # Create a dummy .env if it doesn't exist for standalone testing
    if not os.path.exists(".env"):
        print("Creating dummy .env for menu.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("OWNER_NAME=TestOwnerMenu\n")
            f.write("BOT_NAME=TestBotMenu\n")
    load_env() # Load .env variables
    print(get_menu_text())
    if os.path.exists(".env") and "TestOwnerMenu" in open(".env").read(): # Clean up if dummy was made
        # A bit risky if user has a real .env with this content, but for sandbox it's fine.
        # os.remove(".env")
        # Let's not remove it, it might be the one created by whiz_bot.py earlier.
        pass
