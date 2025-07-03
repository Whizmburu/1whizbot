from utils.env_loader import get_env_variable
# To use the same support group link, we can import it or its source.
# For simplicity, let's import the constant if available, or redefine.
# Option 1: Import from support.py (if it's structured to allow that easily)
try:
    from commands.support import SUPPORT_GROUP_LINK
except ImportError:
    # Fallback if direct import is an issue (e.g. circular dependency if support imports report)
    # Or if support.py doesn't expose it as a direct importable constant.
    # For now, this is a safe fallback.
    SUPPORT_GROUP_LINK = "https://chat.whatsapp.com/JLmSbTfqf4I2Kh4SNJcWgM"

GITHUB_ISSUES_LINK = "https://github.com/WHIZ-MD/Bot/issues"

def get_report_message():
    """Generates the bug reporting information message."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
    owner_name = get_env_variable("OWNER_NAME", "WHIZ") # Used for personalization

    message = f"""
🐞 Found a bug or have an issue with {bot_name}? 🐞

We appreciate your help in making {bot_name} better! Here's how you can report it:

1️⃣ **Via GitHub Issues (Preferred for technical bugs):**
   If you're familiar with GitHub, please open an issue here:
   {GITHUB_ISSUES_LINK}
   Provide as much detail as possible, including steps to reproduce the bug.

2️⃣ **Via our Support Group:**
   You can also report bugs or discuss issues with {owner_name} and the community in our WhatsApp support group:
   {SUPPORT_GROUP_LINK}

Thank you for your contribution!
"""
    return message.strip()

if __name__ == '__main__':
    # For testing the report command module directly
    import os
    from utils.env_loader import load_env
    if not os.path.exists(".env"):
        print("Creating dummy .env for report.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("BOT_NAME=TestBotReport\n")
            f.write("OWNER_NAME=TestOwnerReport\n")
    load_env()
    print(get_report_message())
