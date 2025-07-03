import os
from dotenv import load_dotenv

def load_env():
    """Loads environment variables from .env file."""
    load_dotenv()

def get_env_variable(variable_name, default=None):
    """Gets an environment variable."""
    return os.getenv(variable_name, default)

def validate_session_id():
    """
    Validates the SESSION_ID.
    If it doesn't start with "WHIZ_", it prints a message and exits.
    """
    session_id = get_env_variable("SESSION_ID")
    if not session_id:
        print("🔴 ERROR: SESSION_ID is not set in the .env file.")
        print("Please create a .env file (copy from .env.example) and set your SESSION_ID.")
        print("If you don't have a valid SESSION_ID, visit: https://whizmdsessions.onrender.com")
        exit(1) # Exit if no session ID is found

    if not session_id.startswith("WHIZ_"):
        print("🔴 ERROR: Invalid SESSION_ID.")
        print("Your SESSION_ID must start with 'WHIZ_'.")
        print("Please visit 🔗 https://whizmdsessions.onrender.com to obtain a valid session ID.")
        exit(1) # Exit if session ID is invalid

    return session_id

if __name__ == '__main__':
    # This is for testing the env_loader module directly
    # Create a dummy .env file for testing
    with open(".env", "w") as f:
        f.write("SESSION_ID=INVALID_SESSION\n")
        f.write("OWNER_NAME=TestOwner\n")
        f.write("BOT_NAME=TestBot\n")

    print("Testing with an invalid SESSION_ID (should print error and exit):")
    try:
        load_env()
        validate_session_id()
    except SystemExit as e:
        print(f"Exited with status {e.code} as expected.\n")

    # Test with a valid SESSION_ID
    with open(".env", "w") as f:
        f.write("SESSION_ID=WHIZ_VALID_SESSION_EXAMPLE\n")
        f.write("OWNER_NAME=TestOwner\n")
        f.write("BOT_NAME=TestBot\n")

    print("Testing with a valid SESSION_ID:")
    load_env()
    valid_session_id = validate_session_id()
    print(f"✅ SESSION_ID '{valid_session_id}' is valid.")
    print(f"Bot Name: {get_env_variable('BOT_NAME')}")
    print(f"Owner Name: {get_env_variable('OWNER_NAME')}")

    # Clean up dummy .env file
    if os.path.exists(".env"):
        os.remove(".env")
