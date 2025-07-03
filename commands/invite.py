from utils.env_loader import get_env_variable

def get_invite_message():
    """Generates the bot invite information message."""
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
    # The actual wa.me link would ideally use the bot's phone number.
    # This requires the phone number to be configured, perhaps in .env
    bot_phone_number = get_env_variable("BOT_PHONE_NUMBER", None) # e.g., "15551234567"

    wa_me_link = ""
    if bot_phone_number:
        wa_me_link = f"https://wa.me/{bot_phone_number.replace('+', '').replace(' ', '')}"


    message = f"""
🔗 Want to share {bot_name} or invite it to a group? 🔗

**Sharing with Friends:**
Simply share this bot's contact card/number with your friends. They can then start a chat with {bot_name}.

**Direct Chat Link:**
"""
    if wa_me_link:
        message += f"You can start a direct chat or share this link: {wa_me_link}\n"
    else:
        message += "A direct chat link (wa.me) can be generated if the bot's phone number is configured.\n"
        message += f"For now, please find {bot_name} in your WhatsApp contacts or ask the owner for its number.\n"

    message += f"""
**Adding to Groups:**
1. Add {bot_name}'s number to your phone contacts.
2. Open the WhatsApp group where you want to add the bot.
3. Go to Group Info > Add Participants.
4. Search for {bot_name}'s contact name and add it.

Please ensure you have admin rights in the group to add participants.
Some bots may have restrictions on being added to groups, check with the owner: {get_env_variable('OWNER_NAME', 'the bot owner')}.

Enjoy using {bot_name}!
"""
    return message.strip()

if __name__ == '__main__':
    # For testing the invite command module directly
    import os
    from utils.env_loader import load_env
    if not os.path.exists(".env"):
        print("Creating dummy .env for invite.py direct test")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_test\n")
            f.write("BOT_NAME=TestBotInvite\n")
            f.write("OWNER_NAME=TestOwnerInvite\n")
            # f.write("BOT_PHONE_NUMBER=15551234567\n") # Optional for testing wa.me link
    else:
        # Ensure BOT_PHONE_NUMBER is not accidentally left from previous test if not intended
        # This is tricky, better to manage test .env content explicitly per test run or have separate test .env files
        pass

    load_env()
    print("--- Test Case 1: BOT_PHONE_NUMBER not set ---")
    # To ensure BOT_PHONE_NUMBER is not set for this test case if it exists in .env
    original_phone_num = os.environ.pop('BOT_PHONE_NUMBER', None)
    print(get_invite_message())

    if original_phone_num is not None: # Restore if it was popped
        os.environ['BOT_PHONE_NUMBER'] = original_phone_num

    print("\n--- Test Case 2: BOT_PHONE_NUMBER is set ---")
    # Simulate BOT_PHONE_NUMBER being set for this test
    os.environ['BOT_PHONE_NUMBER'] = "12345678900" # Dummy number for test
    print(get_invite_message())
    del os.environ['BOT_PHONE_NUMBER'] # Clean up test environment variable

    # Clean up dummy .env if we are sure it was created by this specific test run
    # if "TestBotInvite" in open(".env").read():
        # os.remove(".env")
    pass
