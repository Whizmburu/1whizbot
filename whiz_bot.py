# Main file for WHIZ-MD Bot
import time
import os # For dummy .env creation, can be removed later

# Initialize BOT_START_TIME as early as possible
# This is a bit of a workaround to ensure uptime.BOT_START_TIME is set when uptime module is imported by other modules.
# A more robust solution might involve a shared context or explicit initialization function.
import utils.uptime # This will set utils.uptime.BOT_START_TIME

from utils.env_loader import load_env, validate_session_id, get_env_variable
from commands.ping import execute_ping as ping_command_handler
from commands.menu import get_menu_text as menu_command_handler
from commands.stats import get_system_stats as stats_command_handler
from commands.about import get_about_info as about_command_handler
from commands.help import get_help_message as help_command_handler # Added help command

# Store bot's actual start time for uptime calculation consistency
# This shadows the BOT_START_TIME in utils.uptime but ensures it's captured at the true start of whiz_bot.py
# The one in utils.uptime is set upon its first import.
# For simplicity and to avoid confusion, we will primarily rely on the one in utils.uptime.
# The import utils.uptime above should handle this.

def display_connected_message():
    """Displays the WHIZ-MD connected message."""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")

    connected_message = f"""
║️ ✨ {bot_name} CONNECTED ✨ ║️
╔══════════════════════════════════╗
║ 🚀 Status     : Online and Active
║ 📅 Timestamp  : {current_time}
║ 🚫 Errors      : None
╚══════════════════════════════════╝
{bot_name.lower()}
"""
    print(connected_message)

def process_command(command_text):
    """
    Basic command processor.
    In a real bot, this would parse messages from WhatsApp.
    """
    command_received_time = time.time() # Timestamp when command processing starts

    if command_text.lower() == "/ping":
        print(ping_command_handler(command_received_time))
    elif command_text.lower() == "/menu":
        print(menu_command_handler())
    elif command_text.lower() == "/stats":
        print(stats_command_handler())
    elif command_text.lower() == "/about":
        print(about_command_handler())
    elif command_text.lower() == "/help":
        print(help_command_handler())
    else:
        print(f"Unknown command: {command_text}")

def main():
    print("WHIZ-MD Bot Initializing...")

    # Load environment variables
    load_env()

    # Validate Session ID
    session_id = validate_session_id()
    # print(f"✅ SESSION_ID '{session_id[:15]}...' is valid.") # Already printed by validate_session_id on success in some cases, or can be noisy

    bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
    owner_name = get_env_variable("OWNER_NAME", "WHIZ")

    print(f"Bot Name: {bot_name}")
    print(f"Owner Name: {owner_name}")

    # This is where the actual WhatsApp client would connect.
    # For now, we simulate connection success.
    print("Simulating WhatsApp connection...")
    time.sleep(1) # Simulate connection delay
    display_connected_message()

    print("\nType commands to interact with the bot (e.g., /ping, /help). Type 'exit' to quit.")

    # Simulate receiving commands via input (replace with actual WhatsApp message handling later)
    while True:
        try:
            user_input = input(f"[{bot_name}]> ")
            if user_input.lower() == 'exit':
                print("Exiting WHIZ-MD Bot...")
                break
            if user_input.strip(): # If input is not empty
                process_command(user_input.strip())
        except EOFError: # Handle Ctrl+D
            print("\nExiting WHIZ-MD Bot (EOF)...")
            break
        except KeyboardInterrupt: # Handle Ctrl+C
            print("\nExiting WHIZ-MD Bot (Interrupted)...")
            break


if __name__ == "__main__":
    # Create a dummy .env file for demonstration if it doesn't exist
    # In a real scenario, the user must create this.
    if not os.path.exists(".env"):
        print("Note: .env file not found. Creating a dummy one for this run.")
        print("Please create a proper .env file with your SESSION_ID.")
        with open(".env", "w") as f:
            f.write("SESSION_ID=WHIZ_your_whatsapp_session_here\n")
            f.write("OWNER_NAME=WHIZ\n")
            f.write("BOT_NAME=WHIZ-MD\n")
            f.write("OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx\n")
            f.write("PORT=8000\nHOST=0.0.0.0\nMODE=development\n")


    main()
