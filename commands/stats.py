import psutil
import platform

def bytes_to_gb(bytes_val):
    """Converts bytes to gigabytes."""
    return round(bytes_val / (1024**3), 2)

def get_system_stats():
    """
    Gathers system statistics like CPU usage, memory usage, and OS info.
    """
    # CPU Usage
    # cpu_percent() is blocking for the specified interval (in seconds).
    # A non-blocking call (interval=None) would show usage since last call or module import,
    # which might not be what users expect for an "instant" stat.
    # 0.1 seconds is a small compromise.
    cpu_usage = psutil.cpu_percent(interval=0.1)

    # Memory Usage
    memory_info = psutil.virtual_memory()
    total_memory_gb = bytes_to_gb(memory_info.total)
    used_memory_gb = bytes_to_gb(memory_info.used)
    memory_percent = memory_info.percent

    # OS Information
    os_info = f"{platform.system()} {platform.release()}"
    python_version = platform.python_version()

    stats_message = f"""
╔═══════[ 📊 SYSTEM STATS ]═══════╗
║ 💻 OS          : {os_info}
║ 🐍 Python      : {python_version}
║ 🧠 CPU Usage   : {cpu_usage}%
║ 💾 RAM Usage   :
║    Total     : {total_memory_gb} GB
║    Used      : {used_memory_gb} GB ({memory_percent}%)
╚══════════════════════════════════╝
"""
    return stats_message.strip()

if __name__ == '__main__':
    # For testing the stats command module directly
    print("Testing system stats generation...")
    print(get_system_stats())
    # Example with higher CPU usage (simulated by busy work)
    print("\nTesting again after some (simulated) CPU load:")
    for i in range(10**6): # Some computation to make CPU usage non-zero
        pass
    print(get_system_stats())
