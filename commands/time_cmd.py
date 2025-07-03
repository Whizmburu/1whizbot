import datetime
import pytz # For timezone handling

def get_current_time_for_timezone(timezone_str: str = None) -> str:
    """
    Gets the current time for a specified IANA timezone string or server's local time if no timezone is provided.
    Returns a formatted string with the time information or an error message.
    """
    try:
        if timezone_str and timezone_str.strip():
            try:
                # Validate and get the timezone object
                tz = pytz.timezone(timezone_str.strip())
                now_in_tz = datetime.datetime.now(tz)
                # Format: YYYY-MM-DD HH:MM:SS (TZName/Offset) e.g. PST-08:00
                # tzname() can sometimes be None or an abbreviation.
                # utcoffset() gives the offset from UTC.
                offset_seconds = now_in_tz.utcoffset().total_seconds()
                offset_hours = int(offset_seconds // 3600)
                offset_minutes = int((offset_seconds % 3600) // 60)

                # Construct offset string like +HH:MM or -HH:MM
                if offset_hours >= 0:
                    offset_str = f"+{abs(offset_hours):02d}:{abs(offset_minutes):02d}"
                else:
                    offset_str = f"-{abs(offset_hours):02d}:{abs(offset_minutes):02d}"

                # Try to get a common name for the timezone, fallback to the input string or offset
                tz_display_name = now_in_tz.tzname()
                if not tz_display_name or len(tz_display_name) > 5 : # e.g. if it's something like "America/New_York" already
                    tz_display_name = timezone_str.strip()

                return f"🕰️ The current time in {tz_display_name} (UTC{offset_str}) is: \n" \
                       f"{now_in_tz.strftime('%Y-%m-%d %H:%M:%S')}"

            except pytz.exceptions.UnknownTimeZoneError:
                # Provide some suggestions or a link to IANA timezone list
                common_timezones = ["UTC", "US/Eastern", "US/Pacific", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]
                suggestions = ", ".join(common_timezones)
                return f"🚫 Error: Unknown timezone '{timezone_str}'. Please use a valid IANA timezone name.\n" \
                       f"   Examples: {suggestions}\n" \
                       f"   Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            except Exception as e: # Other pytz or datetime errors
                return f"🚫 Error processing timezone '{timezone_str}': {e}"
        else:
            # No timezone provided, use server's local time
            now_local = datetime.datetime.now()
            # Try to get local timezone information (can be system dependent)
            local_tz_name = now_local.astimezone().tzname()
            # Get offset for local time
            local_offset_seconds = now_local.astimezone().utcoffset().total_seconds()
            local_offset_hours = int(local_offset_seconds // 3600)
            local_offset_minutes = int((local_offset_seconds % 3600) // 60)
            if local_offset_hours >= 0:
                local_offset_str = f"+{abs(local_offset_hours):02d}:{abs(local_offset_minutes):02d}"
            else:
                local_offset_str = f"-{abs(local_offset_hours):02d}:{abs(local_offset_minutes):02d}"


            display_name = f"Server Local Time ({local_tz_name}, UTC{local_offset_str})" if local_tz_name else f"Server Local Time (UTC{local_offset_str})"

            return f"🕰️ The current {display_name} is: \n" \
                   f"{now_local.strftime('%Y-%m-%d %H:%M:%S')}"

    except Exception as e:
        # print(f"Time command error: {e}") # For logging
        return f"🚫 Error: Could not retrieve time information. ({e})"

if __name__ == '__main__':
    print("Testing Time Command:\n")

    test_timezones = [
        None, # Server local time
        "UTC",
        "US/Eastern",
        "America/Los_Angeles", # US/Pacific
        "Europe/Paris",
        "Asia/Kolkata",
        "Australia/Melbourne",
        "Invalid/Timezone", # Invalid timezone
        "    Europe/Berlin    ", # With whitespace
        "" # Empty string (should default to local)
    ]

    for i, tz_str in enumerate(test_timezones):
        if tz_str is None:
            print(f"Input {i+1}: (Local Time)")
        else:
            print(f"Input {i+1}: '{tz_str}'")

        result = get_current_time_for_timezone(tz_str)
        print(f"  Output: {result}\n")

    # Test a specific known timezone name behavior
    print("Input: 'EST' (ambiguous, should ideally suggest IANA like US/Eastern)")
    result_est = get_current_time_for_timezone("EST") # EST is not uniquely IANA, pytz might map it or error
    print(f"  Output for EST: {result_est}\n")

    print("Input: 'PST'")
    result_pst = get_current_time_for_timezone("PST")
    print(f"  Output for PST: {result_pst}\n")
