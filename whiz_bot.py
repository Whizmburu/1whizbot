# Main file for WHIZ-MD Bot
import time
import os # For dummy .env creation, can be removed later

# Initialize BOT_START_TIME as early as possible
# This is a bit of a workaround to ensure uptime.BOT_START_TIME is set when uptime module is imported by other modules.
# A more robust solution might involve a shared context or explicit initialization function.
import utils.uptime # This will set utils.uptime.BOT_START_TIME

# Global state for runtime configurations
ACTIVE_PREFIXES = ["/", ".", "#", "whz", "!"] # Default prefixes

from utils.env_loader import load_env, validate_session_id, get_env_variable
from commands.ping import execute_ping as ping_command_handler
from commands.menu import get_menu_text as menu_command_handler
from commands.stats import get_system_stats as stats_command_handler
from commands.about import get_about_info as about_command_handler
from commands.help import get_help_message as help_command_handler
from commands.support import get_support_info as support_command_handler
from commands.prefix import get_prefix_info as prefix_command_handler
from commands.setprefix import update_prefix_list as setprefix_command_handler
from commands.report import get_report_message as report_command_handler
from commands.invite import get_invite_message as invite_command_handler
from commands.calc import evaluate_expression as calc_command_handler
from commands.qr import generate_qr_image as qr_command_handler
from commands.translate import translate_text_command as translate_command_handler # Re-enabled
from commands.shorturl import generate_short_url as shorturl_command_handler
from commands.weather import fetch_weather_data as weather_command_handler
from commands.time_cmd import get_current_time_for_timezone as time_command_handler
from commands.dictionary_cmd import get_word_definition as dictionary_command_handler
from commands.quote_cmd import get_random_quote as quote_command_handler
from commands.fun_cmds import coin_flip as coinflip_command_handler, \
                               magic_8_ball as eight_ball_command_handler, \
                               rate_something as rate_command_handler, \
                               play_rps as rps_command_handler, \
                               get_truth_question as truth_command_handler, \
                               get_dare_challenge as dare_command_handler, \
                               calculate_ship_percentage as ship_command_handler, \
                               guess_the_number as guess_command_handler, \
                               fetch_random_joke as joke_command_handler, \
                               fetch_random_meme as meme_command_handler # Added to fun_cmds
from commands.text_utils_cmds import reverse_text as reverse_command_handler, \
                                     generate_fancy_text as fancy_command_handler, \
                                     generate_zalgo_text as zalgo_command_handler, \
                                     generate_tiny_text as tinytext_command_handler, \
                                     generate_ascii_art as ascii_command_handler, \
                                     find_emojis_for_keyword as emoji_command_handler
from commands.dev_tools_cmds import handle_base64 as base64_command_handler, \
                                     format_json_string as jsonfmt_command_handler, \
                                     fetch_whois_data as whois_command_handler, \
                                     fetch_dns_records as dns_command_handler
from commands.internet_cmds import fetch_wikipedia_summary as wiki_command_handler, \
                                     fetch_github_user_info as github_command_handler, \
                                     fetch_top_headlines as news_command_handler, \
                                     fetch_npm_package_info as npm_command_handler, \
                                     fetch_movie_details as movie_command_handler, \
                                     search_jikan_anime as anime_command_handler
from commands.ai_cmds import get_ai_response as ask_command_handler, \
                               generate_ai_image_from_prompt as imagegen_command_handler, \
                               get_ai_summary as summarize_command_handler, \
                               get_ai_code_generation as codegen_command_handler, \
                               get_ai_chat_response as chat_command_handler
from commands.timing_cmds import start_blocking_timer as timer_command_handler, \
                                 set_reminder_placeholder as reminder_command_handler
from commands.group_admin_cmds import ban_user_placeholder as ban_command_handler, \
                                      kick_user_placeholder as kick_command_handler, \
                                      promote_user_placeholder as promote_command_handler, \
                                      demote_user_placeholder as demote_command_handler, \
                                      mute_user_placeholder as mute_command_handler, \
                                      warn_user_placeholder as warn_command_handler, \
                                      unban_user_placeholder as unban_command_handler, \
                                      get_groupinfo_placeholder as groupinfo_command_handler, \
                                      toggle_antilink_placeholder as antilink_command_handler, \
                                      toggle_lockgroup_placeholder as lockgroup_command_handler
from commands.media_cmds import convert_to_sticker_placeholder as sticker_command_handler, \
                                convert_sticker_to_image_placeholder as toimg_command_handler, \
                                convert_video_to_mp3_placeholder as tomp3_command_handler, \
                                convert_gif_to_sticker_placeholder as gifsticker_command_handler, \
                                remove_image_background_placeholder as removebg_command_handler, \
                                resize_image_placeholder as resize_command_handler, \
                                apply_filter_placeholder as filter_command_handler # Added media_cmds

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
    global ACTIVE_PREFIXES # Declare global at the very start of the function.
    command_received_time = time.time() # Timestamp when command processing starts

    # Command matching logic:
    # For now, we're still using simple direct matches for commands.
    # The ACTIVE_PREFIXES list is managed but not yet used to parse commands.
    # This will be a future refactor.

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
    elif command_text.lower() == "/support":
        print(support_command_handler())
    elif command_text.lower() == "/prefix":
        # Now that ACTIVE_PREFIXES is declared global for the function,
        # this read refers to the global.
        print(prefix_command_handler(ACTIVE_PREFIXES))
    elif command_text.lower().startswith("/setprefix"):
        # No need for another 'global' declaration here.
        parts = command_text.split(maxsplit=1)
        new_prefixes_str = ""
        if len(parts) > 1:
            new_prefixes_str = parts[1]

        new_list, message = setprefix_command_handler(new_prefixes_str)
        if new_list is not None: # Check if update was successful
            ACTIVE_PREFIXES = new_list # Assignment to global
        print(message) # Print success or error message from handler
    elif command_text.lower() == "/report":
        print(report_command_handler())
    elif command_text.lower() == "/invite":
        print(invite_command_handler())
    elif command_text.lower().startswith("/calc"):
        parts = command_text.split(maxsplit=1)
        expression_str = ""
        if len(parts) > 1:
            expression_str = parts[1]
        print(calc_command_handler(expression_str))
    elif command_text.lower().startswith("/qr"):
        parts = command_text.split(maxsplit=1)
        text_to_encode = ""
        if len(parts) > 1:
            text_to_encode = parts[1]
        print(qr_command_handler(text_to_encode))
    elif command_text.lower().startswith("/translate"): # Re-enabled
        parts = command_text.split(maxsplit=1)
        args_str = ""
        if len(parts) > 1:
            args_str = parts[1]
        print(translate_command_handler(args_str))
    elif command_text.lower().startswith("/shorturl"):
        parts = command_text.split(maxsplit=1)
        url_to_shorten = ""
        if len(parts) > 1:
            url_to_shorten = parts[1]
        print(shorturl_command_handler(url_to_shorten))
    elif command_text.lower().startswith("/weather"):
        parts = command_text.split(maxsplit=1)
        location_query = ""
        if len(parts) > 1:
            location_query = parts[1]
        print(weather_command_handler(location_query))
    elif command_text.lower().startswith("/timer"): # Moved /timer before /time
        # /timer <duration> [message]
        parts = command_text.split(maxsplit=1) # Separate command from args
        duration_str_timer = None
        timer_message_str = None
        if len(parts) > 1:
            args_timer = parts[1].strip().split(maxsplit=1) # Split args into duration and message
            if len(args_timer) >= 1:
                duration_str_timer = args_timer[0]
            if len(args_timer) > 1:
                timer_message_str = args_timer[1]
        print(timer_command_handler(duration_str_timer, timer_message_str))
    elif command_text.lower().startswith("/time"):
        parts = command_text.split(maxsplit=1)
        timezone_str = None # Default to None for local time
        if len(parts) > 1:
            timezone_str = parts[1]
        print(time_command_handler(timezone_str))
    elif command_text.lower().startswith("/dictionary"):
        parts = command_text.split(maxsplit=1)
        word_to_define = ""
        if len(parts) > 1:
            word_to_define = parts[1]
        print(dictionary_command_handler(word_to_define))
    elif command_text.lower() == "/quote": # /quote usually doesn't take arguments
        print(quote_command_handler())
    elif command_text.lower() == "/coinflip":
        print(coinflip_command_handler())
    elif command_text.lower().startswith("/8ball"):
        parts = command_text.split(maxsplit=1)
        question_text = None
        if len(parts) > 1:
            question_text = parts[1]
        print(eight_ball_command_handler(question_text))
    elif command_text.lower().startswith("/rate"):
        parts = command_text.split(maxsplit=1)
        item_to_rate = None
        if len(parts) > 1:
            item_to_rate = parts[1]
        print(rate_command_handler(item_to_rate))
    elif command_text.lower().startswith("/rps"):
        parts = command_text.split(maxsplit=1)
        user_choice = None
        if len(parts) > 1:
            user_choice = parts[1]
        print(rps_command_handler(user_choice))
    elif command_text.lower() == "/truth":
        print(truth_command_handler())
    elif command_text.lower() == "/dare":
        print(dare_command_handler())
    elif command_text.lower().startswith("/ship"):
        parts = command_text.split(maxsplit=2) # /ship name1 name2
        name1 = None
        name2 = None
        if len(parts) > 1:
            name1 = parts[1]
        if len(parts) > 2: # This logic is slightly off, split should give 3 parts if two names after /ship
            # Corrected parsing:
            # If /ship name1 name2, parts = ["/ship", "name1", "name2"]
            # If /ship name1, parts = ["/ship", "name1"]
            # If /ship, parts = ["/ship"]
            # The split in the command handler is more robust if we pass the arg string.
            # Let's pass the argument string to the handler.
            arg_str = ""
            if len(command_text.split(maxsplit=1)) > 1:
                arg_str = command_text.split(maxsplit=1)[1]

            # The ship_command_handler expects name1, name2. We need to parse them here.
            name_parts = arg_str.strip().split(maxsplit=1)
            if len(name_parts) >= 1:
                name1 = name_parts[0]
            if len(name_parts) >= 2:
                name2 = name_parts[1]
            print(ship_command_handler(name1, name2)) # Call with potentially None for name2
        else: # Only /ship or /ship name1 was provided
             print(ship_command_handler(name1)) # Let handler deal with name2 being None
    elif command_text.lower().startswith("/guess"):
        parts = command_text.split(maxsplit=1)
        user_guess = None
        if len(parts) > 1:
            user_guess = parts[1]
        print(guess_command_handler(user_guess))
    elif command_text.lower() == "/joke": # /joke doesn't take arguments
        print(joke_command_handler())
    elif command_text.lower().startswith("/meme"):
        parts = command_text.split(maxsplit=1)
        subreddit_meme = None
        if len(parts) > 1:
            subreddit_meme = parts[1] # Optional subreddit
        print(meme_command_handler(subreddit_meme))
    elif command_text.lower().startswith("/reverse"):
        parts = command_text.split(maxsplit=1)
        text_to_reverse = None
        if len(parts) > 1:
            text_to_reverse = parts[1]
        print(reverse_command_handler(text_to_reverse))
    elif command_text.lower().startswith("/fancy"):
        parts = command_text.split(maxsplit=1) # /fancy args
        args_str = None
        if len(parts) > 1:
            args_str = parts[1]

        # Try to parse style and text
        # /fancy <style> <text> OR /fancy <text>
        style_choice = None
        text_to_fancy = None

        if args_str:
            arg_parts = args_str.strip().split(maxsplit=1)
            # Check if first part is a known style (simple check, assumes styles are single words without spaces)
            # A more robust way would be to check against FANCY_STYLES.keys() from text_utils_cmds
            # but that would require importing FANCY_STYLES or passing it around.
            # For now, we assume styles are single words and don't clash with typical text.
            potential_style = arg_parts[0].lower()
            # This is a heuristic: if it's a short word and we have more parts, assume it's a style.
            # Better: `commands.text_utils_cmds.FANCY_STYLES.keys()`
            # For now, the handler `generate_fancy_text` will also try to parse this.
            # Let's pass the full arg string to the handler and let it decide.
            # The handler `generate_fancy_text` is not designed to parse style from text_to_fancy.
            # It expects style_choice and text_to_fancy separately.

            # Re-parsing strategy:
            # First word is potential style. If it's a known style, rest is text.
            # Otherwise, all of args_str is text for default style.
            from commands.text_utils_cmds import FANCY_STYLES as fancy_style_options # Import for check
            if arg_parts[0].lower() in fancy_style_options.keys() and len(arg_parts) > 1:
                style_choice = arg_parts[0].lower()
                text_to_fancy = arg_parts[1]
            else: # First part is not a known style, or only one part given (so it's text)
                text_to_fancy = args_str

        print(fancy_command_handler(text_to_fancy, style_choice))
    elif command_text.lower().startswith("/zalgo"):
        parts = command_text.split(maxsplit=1) # /zalgo args
        args_str = None
        if len(parts) > 1:
            args_str = parts[1]

        intensity = "normal" # Default intensity
        text_to_zalgo = None

        if args_str:
            arg_parts = args_str.strip().split(maxsplit=1)
            # Potential intensities: low, normal, high, max
            potential_intensity = arg_parts[0].lower()
            valid_intensities = ["low", "normal", "high", "max"]
            if potential_intensity in valid_intensities and len(arg_parts) > 1:
                intensity = potential_intensity
                text_to_zalgo = arg_parts[1]
            else: # First part is not a known intensity, or only one part given (so it's text)
                text_to_zalgo = args_str

        print(zalgo_command_handler(text_to_zalgo, intensity))
    elif command_text.lower().startswith("/tinytext"):
        parts = command_text.split(maxsplit=1)
        text_to_tiny = None
        if len(parts) > 1:
            text_to_tiny = parts[1]
        print(tinytext_command_handler(text_to_tiny))
    elif command_text.lower().startswith("/ascii"):
        parts = command_text.split(maxsplit=1) # /ascii args
        args_str = None
        if len(parts) > 1:
            args_str = parts[1]

        font_choice = "standard" # Default font
        text_to_artify = None

        if args_str:
            arg_parts = args_str.strip().split(maxsplit=1)
            # Check if first part is a font (simple check: one word, no spaces, reasonable length)
            # A more robust check would be against pyfiglet.FigletFont.getFonts() or a curated list.
            # For now, the handler `generate_ascii_art` will attempt to use it and catch FontNotFound.
            if len(arg_parts) > 1 and len(arg_parts[0]) < 20 and not " " in arg_parts[0]: # Heuristic for font name
                # Try to see if this font exists, if not, it's part of the text
                # This check is tricky without querying all pyfiglet fonts.
                # Let's assume if there are two parts, first is font, second is text.
                # If one part, it's text. The handler will default font if it's not found.
                # For simplicity in whiz_bot.py, we'll pass font if two args, else just text
                # The generate_ascii_art function itself handles font="standard" default.

                # Simplified parsing: if first word looks like a font name and there's more text.
                # This is similar to /fancy and /zalgo parsing.
                from commands.text_utils_cmds import AVAILABLE_FIGLET_FONTS # For checking
                if arg_parts[0].lower() in AVAILABLE_FIGLET_FONTS and len(arg_parts) > 1:
                    font_choice = arg_parts[0].lower()
                    text_to_artify = arg_parts[1]
                else: # First part is not a known font, or only one part given
                    text_to_artify = args_str
            else: # Only one "word" after /ascii, assume it's text
                 text_to_artify = args_str

        print(ascii_command_handler(text_to_artify, font_choice))
    elif command_text.lower().startswith("/emoji"):
        parts = command_text.split(maxsplit=1)
        keyword = None
        if len(parts) > 1:
            keyword = parts[1]
        print(emoji_command_handler(keyword))
    elif command_text.lower().startswith("/base64"):
        parts = command_text.split(maxsplit=2) # /base64 <action> <string>
        action = None
        input_str = None
        if len(parts) > 1:
            action = parts[1]
        if len(parts) > 2:
            input_str = parts[2]
        print(base64_command_handler(action, input_str))
    elif command_text.lower().startswith("/jsonfmt"):
        parts = command_text.split(maxsplit=1)
        json_str = None
        if len(parts) > 1:
            json_str = parts[1] # The rest of the string is the JSON
        print(jsonfmt_command_handler(json_str))
    elif command_text.lower().startswith("/whois"):
        parts = command_text.split(maxsplit=1)
        domain_name = None
        if len(parts) > 1:
            domain_name = parts[1]
        print(whois_command_handler(domain_name))
    elif command_text.lower().startswith("/dns"):
        parts = command_text.split(maxsplit=2) # /dns <domain> [record_type]
        domain_name_dns = None
        record_type_dns = "A" # Default record type
        if len(parts) > 1:
            domain_name_dns = parts[1]
        if len(parts) > 2:
            record_type_dns = parts[2]
        print(dns_command_handler(domain_name_dns, record_type_dns))
    elif command_text.lower().startswith("/wiki"):
        parts = command_text.split(maxsplit=1)
        query_str = None
        if len(parts) > 1:
            query_str = parts[1]
        print(wiki_command_handler(query_str))
    elif command_text.lower().startswith("/github"):
        parts = command_text.split(maxsplit=1)
        username_gh = None
        if len(parts) > 1:
            username_gh = parts[1]
        print(github_command_handler(username_gh))
    elif command_text.lower().startswith("/news"):
        parts = command_text.split(maxsplit=2) # /news [country] [category]
        # Example: /news us technology -> parts = ["/news", "us", "technology"]
        # Example: /news us -> parts = ["/news", "us"] (category default)
        # Example: /news -> parts = ["/news"] (country and category default)

        country_news = None
        category_news = None

        args_after_command = parts[1] if len(parts) > 1 else ""

        if args_after_command:
            arg_parts_news = args_after_command.strip().split(maxsplit=1)
            # First arg could be country or category if only one is provided.
            # For simplicity, we'll assume if one arg, it's country. If two, country then category.
            # A more robust parser would check if arg1 is a valid category if arg2 is missing, etc.
            if len(arg_parts_news) >= 1:
                # Check if the first argument is a 2-letter country code (heuristic)
                # or a common category name. This parsing can be tricky.
                # Let's assume: /news country category OR /news country OR /news category OR /news
                # The `fetch_top_headlines` function has defaults.
                # We can pass up to two arguments, let the handler sort it if it's smart,
                # or we decide here.
                # Simple approach: first word is country, second is category.
                # If only one word, it's country.
                # This isn't ideal as user might type /news technology (meaning category)

                # Let's try this: first word is country, second is category.
                # If only one word, it's treated as country by default by the handler.
                # The handler has defaults for country ("us") and category ("general").

                country_news = arg_parts_news[0]
                if len(arg_parts_news) > 1:
                    category_news = arg_parts_news[1]

        # The handler defaults country to "us" and category to "general" if None is passed
        print(news_command_handler(country=country_news, category=category_news))
    elif command_text.lower().startswith("/npm"):
        parts = command_text.split(maxsplit=1)
        package_name_npm = None
        if len(parts) > 1:
            package_name_npm = parts[1]
        print(npm_command_handler(package_name_npm))
    elif command_text.lower().startswith("/movie"):
        parts = command_text.split(maxsplit=1)
        movie_title_query = None
        if len(parts) > 1:
            movie_title_query = parts[1]
        print(movie_command_handler(movie_title_query))
    elif command_text.lower().startswith("/anime"):
        parts = command_text.split(maxsplit=1)
        anime_query_str = None
        if len(parts) > 1:
            anime_query_str = parts[1]
        print(anime_command_handler(anime_query_str))
    elif command_text.lower().startswith("/ask"):
        parts = command_text.split(maxsplit=1)
        prompt_str = None
        if len(parts) > 1:
            prompt_str = parts[1]
        print(ask_command_handler(prompt_str))
    elif command_text.lower().startswith("/imagegen"):
        parts = command_text.split(maxsplit=1)
        image_prompt_str = None
        if len(parts) > 1:
            image_prompt_str = parts[1]
        # For now, using default n, size, model.
        # These could be parsed from args_str if desired later.
        print(imagegen_command_handler(image_prompt_str))
    elif command_text.lower().startswith("/summarize"):
        parts = command_text.split(maxsplit=1)
        args_str_summarize = None
        if len(parts) > 1:
            args_str_summarize = parts[1]

        length_option = "medium" # Default
        text_to_summarize = None

        if args_str_summarize:
            arg_parts_summarize = args_str_summarize.strip().split(maxsplit=1)
            potential_length_opt = arg_parts_summarize[0].lower()
            valid_length_opts = ["short", "medium", "long"]

            if potential_length_opt in valid_length_opts and len(arg_parts_summarize) > 1:
                length_option = potential_length_opt
                text_to_summarize = arg_parts_summarize[1]
            else: # First part is not a known length option, or only one part given
                text_to_summarize = args_str_summarize

        print(summarize_command_handler(text_to_summarize, length_option))
    elif command_text.lower().startswith("/codegen"):
        parts = command_text.split(maxsplit=1) # /codegen [lang] <desc>
        args_str_codegen = None
        if len(parts) > 1:
            args_str_codegen = parts[1]

        target_lang_codegen = None
        code_desc_codegen = None

        if args_str_codegen:
            arg_parts_codegen = args_str_codegen.strip().split(maxsplit=1)
            # Simple check: if first word is short (<=10 chars, no spaces) and there's a second part, assume it's a language.
            # This is a heuristic. A list of common languages could be used for better checking.
            if len(arg_parts_codegen) > 1 and len(arg_parts_codegen[0]) <= 10 and not " " in arg_parts_codegen[0]:
                target_lang_codegen = arg_parts_codegen[0]
                code_desc_codegen = arg_parts_codegen[1]
            else: # Assume all of it is description
                code_desc_codegen = args_str_codegen

        print(codegen_command_handler(code_desc_codegen, target_lang_codegen))
    elif command_text.lower().startswith("/chat"):
        parts = command_text.split(maxsplit=1)
        user_chat_message = None
        if len(parts) > 1:
            user_chat_message = parts[1]
        print(chat_command_handler(user_chat_message))
    elif command_text.lower().startswith("/timer"):
        # /timer <duration> [message]
        parts = command_text.split(maxsplit=1) # Separate command from args
        duration_str_timer = None
        timer_message_str = None
        if len(parts) > 1:
            args_timer = parts[1].strip().split(maxsplit=1) # Split args into duration and message
            if len(args_timer) >= 1:
                duration_str_timer = args_timer[0]
            if len(args_timer) > 1:
                timer_message_str = args_timer[1]
        print(timer_command_handler(duration_str_timer, timer_message_str))
    elif command_text.lower().startswith("/reminder"):
        # /reminder <time_specifier> <message>
        # e.g. /reminder in 10m Call mom
        parts = command_text.split(maxsplit=1) # Separate command from args
        time_spec_str_reminder = None
        reminder_message_text = None
        if len(parts) > 1:
            args_reminder = parts[1].strip().split(maxsplit=1) # Split args into time_spec and message
            # First part of args_reminder must be "in" for the simple parser
            if len(args_reminder) >= 1 and args_reminder[0].lower() == "in":
                if len(args_reminder) > 1: # We have "in" and potentially "10m Call mom"
                    # Re-split the second part to get duration and message
                    duration_and_msg_parts = args_reminder[1].split(maxsplit=1)
                    time_spec_str_reminder = f"in {duration_and_msg_parts[0]}"
                    if len(duration_and_msg_parts) > 1:
                        reminder_message_text = duration_and_msg_parts[1]
                    else: # Only "in <duration>" was provided, missing message
                        # The handler will catch missing message
                        pass
                # else: only "/reminder in" was typed, handler will catch missing time_spec/message
            else: # Does not start with "in", pass full args to handler for it to error
                # Or, it's just "/reminder some message without 'in'"
                # For simplicity, the handler expects "in ..." for time_spec
                # So, if not "in", likely invalid time_spec or just reminder_text for a default time (not supported by current placeholder)
                # Pass the first part as time_spec and rest as message
                if len(args_reminder) >=1:
                    time_spec_str_reminder = args_reminder[0] # Will likely fail in handler if not "in ..."
                if len(args_reminder) > 1:
                    reminder_message_text = args_reminder[1]


        print(reminder_command_handler(time_spec_str_reminder, reminder_message_text))
    elif command_text.lower().startswith("/ban"):
        # /ban <user_id> [reason]
        parts = command_text.split(maxsplit=1) # Separate command from args
        user_to_ban = None
        reason_for_ban = None
        if len(parts) > 1:
            args_ban = parts[1].strip().split(maxsplit=1) # Split args into user_id and reason
            if len(args_ban) >= 1:
                user_to_ban = args_ban[0]
            if len(args_ban) > 1:
                reason_for_ban = args_ban[1]
        print(ban_command_handler(user_to_ban, reason_for_ban))
    elif command_text.lower().startswith("/kick"):
        # /kick <user_id> [reason]
        parts = command_text.split(maxsplit=1)
        user_to_kick = None
        reason_for_kick = None
        if len(parts) > 1:
            args_kick = parts[1].strip().split(maxsplit=1)
            if len(args_kick) >= 1:
                user_to_kick = args_kick[0]
            if len(args_kick) > 1:
                reason_for_kick = args_kick[1]
        print(kick_command_handler(user_to_kick, reason_for_kick))
    elif command_text.lower().startswith("/promote"):
        parts = command_text.split(maxsplit=1)
        user_to_promote = None
        if len(parts) > 1:
            user_to_promote = parts[1].strip() # Promote takes only one arg (user)
        print(promote_command_handler(user_to_promote))
    elif command_text.lower().startswith("/demote"):
        parts = command_text.split(maxsplit=1)
        user_to_demote = None
        if len(parts) > 1:
            user_to_demote = parts[1].strip() # Demote takes only one arg (user)
        print(demote_command_handler(user_to_demote))
    elif command_text.lower().startswith("/mute"):
        # /mute <user_id> [duration]
        parts = command_text.split(maxsplit=1)
        user_to_mute = None
        duration_for_mute = None
        if len(parts) > 1:
            args_mute = parts[1].strip().split(maxsplit=1)
            if len(args_mute) >= 1:
                user_to_mute = args_mute[0]
            if len(args_mute) > 1:
                duration_for_mute = args_mute[1]
        print(mute_command_handler(user_to_mute, duration_for_mute))
    elif command_text.lower().startswith("/warn"):
        # /warn <user_id> [reason]
        parts = command_text.split(maxsplit=1)
        user_to_warn = None
        reason_for_warn = None
        if len(parts) > 1:
            args_warn = parts[1].strip().split(maxsplit=1)
            if len(args_warn) >= 1:
                user_to_warn = args_warn[0]
            if len(args_warn) > 1:
                reason_for_warn = args_warn[1]
        print(warn_command_handler(user_to_warn, reason_for_warn))
    elif command_text.lower().startswith("/unban"):
        parts = command_text.split(maxsplit=1)
        user_to_unban = None
        if len(parts) > 1:
            user_to_unban = parts[1].strip() # Unban takes only one arg (user)
        print(unban_command_handler(user_to_unban))
    elif command_text.lower() == "/groupinfo": # No arguments needed for groupinfo
        print(groupinfo_command_handler())
    elif command_text.lower().startswith("/antilink"):
        parts = command_text.split(maxsplit=1)
        toggle_value_antilink = None
        if len(parts) > 1:
            toggle_value_antilink = parts[1].strip()
        print(antilink_command_handler(toggle_value_antilink))
    elif command_text.lower().startswith("/lockgroup"):
        parts = command_text.split(maxsplit=1)
        toggle_value_lockgroup = None
        if len(parts) > 1:
            toggle_value_lockgroup = parts[1].strip()
        print(lockgroup_command_handler(toggle_value_lockgroup))
    elif command_text.lower().startswith("/sticker"):
        parts = command_text.split(maxsplit=1)
        image_path_sticker = None
        if len(parts) > 1:
            image_path_sticker = parts[1].strip() # Path or URL to image
        print(sticker_command_handler(image_path_sticker))
    elif command_text.lower().startswith("/toimg"):
        parts = command_text.split(maxsplit=1)
        sticker_path_toimg = None
        if len(parts) > 1:
            sticker_path_toimg = parts[1].strip() # Path or URL to sticker
        print(toimg_command_handler(sticker_path_toimg))
    elif command_text.lower().startswith("/tomp3"):
        parts = command_text.split(maxsplit=1)
        video_path_tomp3 = None
        if len(parts) > 1:
            video_path_tomp3 = parts[1].strip() # Path or URL to video
        print(tomp3_command_handler(video_path_tomp3))
    elif command_text.lower().startswith("/gifsticker"):
        parts = command_text.split(maxsplit=1)
        gif_path_sticker = None
        if len(parts) > 1:
            gif_path_sticker = parts[1].strip() # Path or URL to GIF
        print(gifsticker_command_handler(gif_path_sticker))
    elif command_text.lower().startswith("/removebg"):
        parts = command_text.split(maxsplit=1)
        image_path_removebg = None
        if len(parts) > 1:
            image_path_removebg = parts[1].strip() # Path or URL to image
        print(removebg_command_handler(image_path_removebg))
    elif command_text.lower().startswith("/resize"):
        # /resize <image_path> [dimensions_str]
        parts = command_text.split(maxsplit=1)
        image_path_resize = None
        dimensions_resize = None
        if len(parts) > 1:
            args_resize = parts[1].strip().split(maxsplit=1)
            if len(args_resize) >= 1:
                image_path_resize = args_resize[0]
            if len(args_resize) > 1:
                dimensions_resize = args_resize[1]
        print(resize_command_handler(image_path_resize, dimensions_resize))
    elif command_text.lower().startswith("/filter"):
        # /filter <image_path> [filter_name]
        parts = command_text.split(maxsplit=1)
        image_path_filter = None
        filter_name_str = None
        if len(parts) > 1:
            args_filter = parts[1].strip().split(maxsplit=1)
            if len(args_filter) >= 1:
                image_path_filter = args_filter[0]
            if len(args_filter) > 1:
                filter_name_str = args_filter[1]
        print(filter_command_handler(image_path_filter, filter_name_str))
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
