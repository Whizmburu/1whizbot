import time
import os
from utils.uptime import get_uptime

def get_load_avg():
    """Gets system load average. Placeholder for now."""
    # os.getloadavg() is available on Unix-like systems.
    # For Windows, this would require a different approach (e.g., psutil library)
    try:
        if hasattr(os, 'getloadavg'):
            load1, load5, load15 = os.getloadavg()
            return f"{load1:.2f}, {load5:.2f}, {load15:.2f}"
        else:
            return "N/A (Windows)"
    except OSError:
        return "N/A"

def execute_ping(start_time):
    """
    Generates the ping message.
    `start_time` is the timestamp when the command was received.
    """
    ping_time_ms = (time.time() - start_time) * 1000
    uptime = get_uptime()
    load_avg = get_load_avg() # This is a system load average, not specific to the bot process.

    # Determine speed based on ping_time_ms
    if ping_time_ms < 100:
        speed = "Excellent"
    elif ping_time_ms < 300:
        speed = "Good"
    elif ping_time_ms < 700:
        speed = "Moderate"
    else:
        speed = "Slow"

    ping_message = f"""
╔═══════[ 📡 PING STATUS ]═══════╗
║ 🔪 Response    : {ping_time_ms:.2f}ms
║ ⚡ Speed       : {speed}
║ 📊 Uptime      : {uptime}
║ 🩸 Load        : {load_avg}
╚══════════════════════════════════╝
"""
    return ping_message

if __name__ == '__main__':
    # This is for testing the ping command module directly
    print("Testing ping command execution...")
    # Simulate command received time
    test_start_time = time.time()
    # Simulate some processing delay
    time.sleep(0.05)
    print(execute_ping(test_start_time))

    print("\nTesting uptime function from ping module context:")
    # To ensure BOT_START_TIME in uptime.py is initialized when uptime.py is imported
    # we need to import it in a context where BOT_START_TIME is set.
    # For this direct test, uptime starts when uptime.py was first imported.
    # If uptime.py was just created, its BOT_START_TIME is very recent.
    print(f"Uptime from imported get_uptime(): {get_uptime()}")

    # Test load average (behavior depends on OS)
    print(f"\nSystem Load Average: {get_load_avg()}")
