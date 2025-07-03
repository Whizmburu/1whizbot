import qrcode # The main library
import os # For path manipulation
from utils.env_loader import get_env_variable # For bot name, if needed in messages

# Define a directory to store generated QR codes.
# It's good practice to have a dedicated, possibly temporary, place.
QR_CODE_DIR = "qr_codes"
# Ensure this directory exists when the module is loaded or when function is called.

def ensure_qr_code_dir_exists():
    """Checks if QR_CODE_DIR exists, creates it if not."""
    if not os.path.exists(QR_CODE_DIR):
        try:
            os.makedirs(QR_CODE_DIR)
            # print(f"Created directory: {QR_CODE_DIR}") # For debugging
        except OSError as e:
            # print(f"Error creating directory {QR_CODE_DIR}: {e}") # For debugging
            # If directory creation fails, we might not be able to save QR codes.
            # The function will still try to save, and qrcode.save() might fail.
            pass # Let the save operation handle the error if dir creation failed silently.

def generate_qr_image(text_to_encode: str) -> str:
    """
    Generates a QR code image from the given text and saves it to a file.
    Returns a message string (path to file or error message).
    """
    ensure_qr_code_dir_exists() # Make sure directory exists

    if not text_to_encode:
        return "🚫 Error: No text provided to generate QR code. Usage: /qr <your text here>"

    # Basic sanitization for filename (replace non-alphanumeric with underscore)
    # And truncate to avoid overly long filenames.
    safe_filename_base = "".join(c if c.isalnum() else "_" for c in text_to_encode[:30])
    if not safe_filename_base: # If text was all non-alphanumeric or empty after slice
        safe_filename_base = "qr_code"

    filename = f"{safe_filename_base}.png"
    filepath = os.path.join(QR_CODE_DIR, filename)

    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1, # Controls the size of the QR Code, 1 is smallest (21x21)
            error_correction=qrcode.constants.ERROR_CORRECT_L, # L = Low (about 7% or less errors can be corrected)
            box_size=10, # Size of each "box" in pixels
            border=4,    # Thickness of the border (minimum is 4 for spec)
        )
        qr.add_data(text_to_encode)
        qr.make(fit=True) # Ensure the entire QR code fits

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        img.save(filepath)

        bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
        return f"✅ QR Code generated successfully for '{text_to_encode[:50]}{'...' if len(text_to_encode)>50 else ''}'!\n" \
               f"🖼️ Saved as: {filepath}\n" \
               f"(In a real WhatsApp bot, {bot_name} would send the image directly.)"

    except FileNotFoundError: # If QR_CODE_DIR still doesn't exist and save fails
        return f"🚫 Error: Could not save QR code. Directory '{QR_CODE_DIR}' might be inaccessible."
    except Exception as e:
        # print(f"QR generation error: {e}") # For logging/debugging
        return f"🚫 Error: Could not generate QR code. Details: {str(e)}"

if __name__ == '__main__':
    print("Testing QR Code generation:\n")

    test_texts = [
        "Hello, WHIZ-MD Bot!",
        "https://github.com/WHIZ-MD/Bot",
        "1234567890",
        "", # Empty string test
        "A very long string to test filename truncation and QR code capacity if it were much longer than this example which is actually not that long for a QR code to handle but good for filename testing perhaps.",
        "!@#$%^&*()_+=-`~[]{};':\",./<>?", # Special characters
    ]

    for i, text in enumerate(test_texts):
        print(f"Input {i+1}: '{text}'")
        output_message = generate_qr_image(text)
        print(f"  Output: {output_message}\n")
        # To verify, you'd check if the file exists in qr_codes/ directory
        # e.g., if text is "Hello...", filename might be "Hello__________.png"

    # Example of checking a file (optional, for manual verification during test)
    if os.path.exists(os.path.join(QR_CODE_DIR, "Hello_WHIZ_MD_Bot.png")):
        print(f"File '{os.path.join(QR_CODE_DIR, 'Hello_WHIZ_MD_Bot.png')}' seems to be created.")

    # Clean up created qr_codes directory and files after test (optional)
    # import shutil
    # if os.path.exists(QR_CODE_DIR):
    #     try:
    #         shutil.rmtree(QR_CODE_DIR)
    #         print(f"Cleaned up directory: {QR_CODE_DIR}")
    #     except OSError as e:
    #         print(f"Error cleaning up directory {QR_CODE_DIR}: {e}")
