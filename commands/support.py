from utils.env_loader import get_env_variable

SUPPORT_GROUP_LINK = "https://chat.whatsapp.com/JLmSbTfqf4I2Kh4SNJcWgM"

def get_support_info():
    """Generates the support information message."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    message = f"""
📞 Need help, have suggestions, or just want to join the {bot_name} community?

Join our official WhatsApp Support Group:
{SUPPORT_GROUP_LINK}

We're always happy to help!
"""
    return message.strip()

if __name__ == '__main__':
    # For testing the support command module directly
    import os
    from utils.env_loader import load_env
    if not os.path.exists(".env"):
        print("Creating dummy .env for support.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("BOT_NAME=TestBotSupport\n")
    load_env()
    print(get_support_info())
