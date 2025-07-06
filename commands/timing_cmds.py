import time
import re

# --- Timer Command (Blocking Version) ---

def parse_duration_to_seconds(duration_str: str) -> int | None:
    """
    Parses a duration string (e.g., "30s", "5m", "1h", "1h30m15s") into total seconds.
    Returns total seconds if valid, else None.
    """
    if not duration_str or not duration_str.strip():
        return None

    duration_str = duration_str.strip().lower()
    total_seconds = 0

    # Regex to find components like 1h, 30m, 15s
    # Using findall to capture all components
    parts = re.findall(r'(\d+)([hms])', duration_str)

    if not parts: # No valid parts found
        # Try to parse if it's just a number (assume seconds)
        if duration_str.isdigit():
            return int(duration_str)
        return None

    parsed_anything = False
    for value, unit in parts:
        value = int(value)
        if unit == 'h':
            total_seconds += value * 3600
            parsed_anything = True
        elif unit == 'm':
            total_seconds += value * 60
            parsed_anything = True
        elif unit == 's':
            total_seconds += value
            parsed_anything = True

    # Check if the entire string was parsed by these components
    # This is a bit tricky with findall if there's other text.
    # A simpler check: if we parsed something and the sum is > 0
    if not parsed_anything and not (duration_str.isdigit() and int(duration_str) > 0) :
         return None # If no h, m, or s units were found and it's not just seconds

    # Check if the string *only* contained valid duration parts.
    # Reconstruct what was parsed and compare.
    # Example: "1h30m" -> "1h30m", "1h 30m" -> "1h30m" (after stripping spaces in a more complex regex)
    # For now, this regex is fine, but it won't reject "1h30m_invalid_text"
    # A stricter regex for the whole string would be: ^(\d+h)?(\d+m)?(\d+s)?$
    # but the current findall is more flexible for inputs like "1h 30m".

    if total_seconds <= 0: # Must be a positive duration
        return None

    return total_seconds

def start_blocking_timer(duration_str: str, timer_message: str = None) -> str:
    """
    Starts a blocking timer for the specified duration.
    """
    if not duration_str:
        return "⏳ Please specify a duration for the timer. Usage: /timer <duration> [message]\n" \
               "   Duration format: e.g., 30s, 5m, 1h, 1h30m, 2m10s"

    total_seconds = parse_duration_to_seconds(duration_str)

    if total_seconds is None:
        return f"🚫 Invalid duration format: '{duration_str}'.\n" \
               "   Use 'h', 'm', 's' (e.g., 1h30m, 5m, 30s)."

    if total_seconds > 3600 * 3: # Arbitrary limit, e.g., 3 hours for a blocking timer
        return "🚫 Timer duration is too long for a blocking timer (max 3 hours). Please use a shorter duration."

    message_on_finish = timer_message if timer_message and timer_message.strip() else "Timer finished!"

    # Get a human-readable version of total_seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    readable_duration_parts = []
    if hours > 0: readable_duration_parts.append(f"{hours}h")
    if minutes > 0: readable_duration_parts.append(f"{minutes}m")
    if seconds > 0 or not readable_duration_parts : readable_duration_parts.append(f"{seconds}s") # Show 0s if no h/m
    readable_duration = "".join(readable_duration_parts)


    # Inform user, then block
    # In a real bot, this message would be sent, then the bot would do other things
    # before the timer callback. Here, it's just a print before sleep.
    initial_message = f"⏳ Timer started for {readable_duration}. " \
                      f"The bot will be unresponsive to other commands until the timer is up.\n" \
                      f"   You asked to be reminded of: \"{message_on_finish}\""
    print(initial_message) # Simulate sending this message first

    try:
        time.sleep(total_seconds)
        return f"⏰ **Timer Up!** ({readable_duration})\n   Your message: \"{message_on_finish}\""
    except KeyboardInterrupt:
        return "🛑 Timer interrupted by user." # Should not happen in normal bot flow
    except Exception as e:
        return f"🚫 Error during timer: {e}"


if __name__ == '__main__':
    print("--- Testing Timing Commands ---\n")

    print("Testing parse_duration_to_seconds:")
    durations_to_test = ["30s", "5m", "1h", "1h30m", "2m15s", "1h1m1s", "10", "abc", "1h30mInvalid", "0s", "-5m"]
    for d_str in durations_to_test:
        secs = parse_duration_to_seconds(d_str)
        print(f"  Input: '{d_str}' -> Seconds: {secs}")
    print("-" * 20 + "\n")

    print("Testing start_blocking_timer:")
    print("  Test 1 (5s, default message):")
    # print(start_blocking_timer("5s")) # This will block tests, run manually if needed
    # For automated test, we check the setup message and error cases
    print(f"    (Simulating call with '5s') -> Would block for 5s then print 'Timer Up! Your message: \"Timer finished!\"'")

    print("\n  Test 2 (3s, custom message):")
    # print(start_blocking_timer("3s", "Time for a break!"))
    print(f"    (Simulating call with '3s', 'Time for a break!') -> Would block for 3s then print 'Timer Up! Your message: \"Time for a break!\"'")

    print(f"\n  Test 3 (invalid duration): {start_blocking_timer('invalid')}")
    print(f"  Test 4 (no duration): {start_blocking_timer(None)}")
    print(f"  Test 5 (too long duration): {start_blocking_timer('4h')}") # 4 hours
    print(f"  Test 6 (just seconds as number): {start_blocking_timer('10')}") # Should print initial message then would block
    print("-" * 20 + "\n")

# --- Reminder Command (Placeholder / Acknowledgement Only) ---

def parse_reminder_time_specifier(time_spec_str: str) -> tuple[str | None, int | None]:
    """
    Parses a simple time specifier like "in 10m", "in 1h30m".
    Returns a tuple: (human_readable_duration_str, total_seconds_from_now).
    Returns (None, None) if parsing fails.
    This is a simplified version for the placeholder.
    """
    if not time_spec_str or not time_spec_str.strip().lower().startswith("in "):
        return None, None # Expects "in ..." format for now

    duration_part = time_spec_str.strip()[3:] # Get the part after "in "

    total_seconds = parse_duration_to_seconds(duration_part)
    if total_seconds is None:
        return None, None

    # Create a human-readable version for the acknowledgement message
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    readable_duration_parts = []
    if hours > 0: readable_duration_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0: readable_duration_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0: readable_duration_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    if not readable_duration_parts: # e.g. if duration was "0s" or invalid leading to 0
        return None, None # Should be caught by parse_duration_to_seconds returning None for total_seconds <=0

    human_readable_duration = ", ".join(readable_duration_parts)
    if not human_readable_duration : human_readable_duration = f"{total_seconds} seconds" # Fallback

    return human_readable_duration, total_seconds


def set_reminder_placeholder(time_specifier_str: str, reminder_text: str = None) -> str:
    """
    Acknowledges setting a reminder. Does not actually schedule anything.
    time_specifier_str: e.g., "in 10m", "in 1h30m"
    """
    if not time_specifier_str:
        return "🔔 Please specify when the reminder should be. Usage: /reminder <time_specifier> <message>\n" \
               "   Time specifier examples: 'in 30s', 'in 10m', 'in 1h30m'"

    if not reminder_text or not reminder_text.strip():
        return "🔔 Please provide a message for your reminder. Usage: /reminder <time_specifier> <message>"

    parsed_duration_str, _ = parse_reminder_time_specifier(time_specifier_str)

    if not parsed_duration_str:
        return f"🚫 Invalid time specifier: '{time_specifier_str}'.\n" \
               "   Please use format like 'in 10m', 'in 1h', 'in 30s'."

    return f"✅ Reminder acknowledged for: \"{reminder_text.strip()}\"\n" \
           f"   🔔 To go off in approximately: {parsed_duration_str}.\n" \
           f"(Note: This is a placeholder. Actual background notifications are not yet implemented.)"


if __name__ == '__main__':
    print("--- Testing Timing Commands ---\n")

    # ... (timer tests remain the same) ...
    print("Testing parse_duration_to_seconds:")
    print(f"  Input: '30s' -> Seconds: {parse_duration_to_seconds('30s')}")
    print("-" * 20 + "\n")
    print("Testing start_blocking_timer:")
    print(f"  Test (invalid duration): {start_blocking_timer('invalid')}")
    print("-" * 20 + "\n")

    print("Testing parse_reminder_time_specifier:")
    rem_times_to_test = ["in 10m", "in 1h30s", "in 2h 5m 10s", "10m", "in five minutes", "in 0s"]
    for rt_str in rem_times_to_test:
        readable, secs = parse_reminder_time_specifier(rt_str)
        print(f"  Input: '{rt_str}' -> Readable: '{readable}', Seconds: {secs}")
    print("-" * 20 + "\n")

    print("Testing set_reminder_placeholder:")
    print(f"  Test 1 (valid): {set_reminder_placeholder('in 15m', 'Call Mom')}")
    print(f"  Test 2 (no message): {set_reminder_placeholder('in 10m')}")
    print(f"  Test 3 (no time spec): {set_reminder_placeholder(None, 'Test message')}")
    print(f"  Test 4 (invalid time spec): {set_reminder_placeholder('tomorrow', 'Test message')}")
    print(f"  Test 5 (invalid duration in spec): {set_reminder_placeholder('in 0m', 'Test message')}")
    print(f"  Test 6 (valid complex duration): {set_reminder_placeholder('in 1h5m30s', 'Long meeting')}")

    print("-" * 20 + "\n")
