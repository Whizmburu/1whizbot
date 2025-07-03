import time

BOT_START_TIME = time.time()

def get_uptime():
    """Calculates the bot's uptime."""
    uptime_seconds = time.time() - BOT_START_TIME
    days = int(uptime_seconds // (24 * 3600))
    uptime_seconds %= (24 * 3600)
    hours = int(uptime_seconds // 3600)
    uptime_seconds %= 3600
    minutes = int(uptime_seconds // 60)
    seconds = int(uptime_seconds % 60)

    uptime_str = ""
    if days > 0:
        uptime_str += f"{days}d "
    if hours > 0:
        uptime_str += f"{hours}h "
    if minutes > 0:
        uptime_str += f"{minutes}m "
    uptime_str += f"{seconds}s"

    return uptime_str.strip()

if __name__ == '__main__':
    print(f"Bot started at: {time.ctime(BOT_START_TIME)}")
    print("Waiting for 5 seconds to test uptime...")
    time.sleep(5)
    print(f"Current Uptime: {get_uptime()}")
    print("Waiting for another 65 seconds to test uptime (total > 1 min)...")
    time.sleep(65)
    print(f"Current Uptime: {get_uptime()}")
