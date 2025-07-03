import random

# --- Coinflip Command ---
def coin_flip() -> str:
    """
    Simulates a coin flip.
    Returns a string indicating "Heads" or "Tails".
    """
    outcomes = ["Heads", "Tails"]
    result = random.choice(outcomes)

    # Adding some visual flair
    if result == "Heads":
        emoji = "👑" # Or any head-like emoji
        message = f"🪙 The coin landed on: **{result}**! {emoji}"
    else:
        emoji = "🦅" # Tails often has an eagle or similar emblem
        message = f"🪙 The coin landed on: **{result}**! {emoji}"

    return message

# --- Magic 8-Ball Command ---
EIGHT_BALL_ANSWERS = [
    # Affirmative
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes – definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    # Non-committal
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    # Negative
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
]

def magic_8_ball(question_text: str = None) -> str:
    """
    Provides a random Magic 8-Ball answer to a user's question.
    """
    if not question_text or not question_text.strip():
        return "🎱 Please ask a yes/no question after the /8ball command! (e.g., /8ball Will I be rich?)"

    # Optionally, check if the question ends with a question mark
    # if not question_text.strip().endswith("?"):
    #     return "🎱 That doesn't sound like a question! Try ending it with a '?'."

    answer = random.choice(EIGHT_BALL_ANSWERS)
    return f"🎱 You asked: \"{question_text.strip()}\"\nMagic 8-Ball says: **\"{answer}\"**"

# --- Rate Command ---
def rate_something(item_to_rate: str = None) -> str:
    """
    Rates a given item (or a generic concept if no item provided) on a scale of 0-100.
    """
    if not item_to_rate or not item_to_rate.strip():
        # Generic item if nothing specific is provided
        item_to_rate = "your general vibe today"
    else:
        item_to_rate = item_to_rate.strip()
        # Optional: add "my" or "your" if not present for better phrasing
        # if not item_to_rate.lower().startswith(("my ", "your ")):
        #    item_to_rate = f"'{item_to_rate}'" # Just quote it if not personal

    score = random.randint(0, 100) # Inclusive range

    # Add some qualitative feedback based on score
    feedback = ""
    if score == 100:
        feedback = "Absolutely perfect! 🌟"
    elif score >= 90:
        feedback = "Outstanding! ✨"
    elif score >= 80:
        feedback = "Great stuff! 👍"
    elif score >= 70:
        feedback = "Pretty good! 😊"
    elif score >= 60:
        feedback = "Not bad, not bad."
    elif score >= 40:
        feedback = "Hmm, could be better. 🤔"
    elif score >= 20:
        feedback = "Needs some work. 😬"
    elif score > 0:
        feedback = "Oof, tough one. 😥"
    else: # score == 0
        feedback = "Yikes... 💀 Zero? That's harsh!"

    return f"🤔 After careful consideration, I'd rate {item_to_rate} a **{score}/100**! {feedback}"

# --- Rock Paper Scissors (RPS) Command ---
RPS_CHOICES = ["rock", "paper", "scissors"]
RPS_EMOJIS = {
    "rock": "✊",
    "paper": "✋",
    "scissors": "✌️"
}
RPS_RULES = {
    ("rock", "scissors"): "You Win!",   # Rock smashes scissors
    ("scissors", "paper"): "You Win!", # Scissors cuts paper
    ("paper", "rock"): "You Win!",    # Paper covers rock
    ("scissors", "rock"): "I Win!",
    ("paper", "scissors"): "I Win!",
    ("rock", "paper"): "I Win!"
}

def play_rps(user_choice_str: str = None) -> str:
    """
    Plays a game of Rock, Paper, Scissors with the user.
    """
    if not user_choice_str or not user_choice_str.strip():
        return "🪨📄✂️ Choose rock, paper, or scissors! Usage: /rps <your_choice>"

    user_choice = user_choice_str.strip().lower()
    if user_choice not in RPS_CHOICES:
        return f"🤨 Invalid choice: '{user_choice}'. Please choose rock, paper, or scissors."

    bot_choice = random.choice(RPS_CHOICES)

    user_emoji = RPS_EMOJIS.get(user_choice, "")
    bot_emoji = RPS_EMOJIS.get(bot_choice, "")

    result_message = ""
    if user_choice == bot_choice:
        result_message = "It's a Tie!"
    else:
        result_message = RPS_RULES.get((user_choice, bot_choice), "Error in game logic!") # Fallback

    return f"You chose: {user_choice.capitalize()} {user_emoji}\n" \
           f"I chose: {bot_choice.capitalize()} {bot_emoji}\n\n" \
           f"🎉 **{result_message}** 🎉"

# --- Truth Command ---
TRUTH_QUESTIONS = [
    "What's the most embarrassing thing that's happened to you this month?",
    "Have you ever cheated on a test?",
    "What's a secret you've never told anyone?",
    "What's your biggest fear?",
    "Who is your secret crush?",
    "What's the last lie you told?",
    "What's something you regret doing?",
    "What's the weirdest dream you've ever had?",
    "If you could trade lives with someone for a day, who would it be and why?",
    "What's one thing you would change about your appearance if you could?",
    "What's a bad habit you're trying to break?",
    "Have you ever pretended to be sick to avoid something?",
    "What's the silliest thing you've ever done for love?",
    "What's your most prized possession and why?",
    "If you had to delete all but one app from your phone, which one would you keep?"
]

def get_truth_question() -> str:
    """
    Provides a random truth question.
    """
    question = random.choice(TRUTH_QUESTIONS)
    return f"❓ **Truth:** {question}"

# --- Dare Command ---
DARE_CHALLENGES = [
    "Sing the chorus of your current favorite song out loud.",
    "Do 10 jumping jacks right now.",
    "Talk in a funny accent for the next 5 messages.",
    "Send a voice message saying 'I am a potato'.",
    "Try to lick your elbow.",
    "Post 'I love pineapples on pizza' as your status (if you dare!).",
    "Text your best friend a random animal emoji without any explanation.",
    "Wear socks on your hands for the next 10 minutes.",
    "Attempt to juggle 3 small objects.",
    "Speak only in questions for the next 3 messages you send.",
    "Send an GIPHY/image of the first thing that comes to your mind when you read 'banana'.",
    "Tell a short, clean joke.",
    "Change your profile picture to a picture of a rubber duck for 1 hour.",
    "Try to balance a spoon on your nose for 30 seconds.",
    "Spell your name backwards as fast as you can."
]

def get_dare_challenge() -> str:
    """
    Provides a random dare challenge.
    """
    dare = random.choice(DARE_CHALLENGES)
    return f"🔥 **Dare:** {dare}"

# --- Ship (Love Calculator) Command ---
def calculate_ship_percentage(name1_str: str, name2_str: str = None) -> str:
    """
    Calculates a 'love compatibility' percentage between two names.
    If only one name is provided, it ships with the bot.
    """
    from utils.env_loader import get_env_variable # Delayed import if needed

    if not name1_str or not name1_str.strip():
        return "💖 Please provide at least one name to ship! Usage: /ship <name1> [name2]"

    name1 = name1_str.strip().title() # Capitalize for display

    if not name2_str or not name2_str.strip():
        bot_name = get_env_variable("BOT_NAME", "WHIZ-MD")
        name2 = bot_name
        if name1.lower() == name2.lower(): # User entered bot's name as name1
             return f"💖 Trying to ship {name1} with itself? That's a solid 100% self-love! Or did you mean to ship with someone else?"
    else:
        name2 = name2_str.strip().title()

    if name1.lower() == name2.lower():
        # Handle cases like /ship Alice Alice
        return f"💖 Shipping {name1} with {name2}? That's a perfect match of **100%**! Self-love is important, or maybe it's true love with an identical twin! 😉"

    # Simple deterministic algorithm based on names for fun
    # Sort names to ensure ship(A,B) == ship(B,A) for percentage
    sorted_names = sorted([name1.lower(), name2.lower()])
    combined_names = "".join(sorted_names)

    # Use a seed based on the combined names for consistent randomness if random is used
    # For a simple sum-of-ords approach:
    love_score = sum(ord(c) for c in combined_names) % 101 # Max 100%

    feedback = ""
    if love_score == 100:
        feedback = "A perfect match made in heaven! 🌟💍"
    elif love_score >= 90:
        feedback = "Wow, true soulmates! ❤️🔥"
    elif love_score >= 80:
        feedback = "Amazing compatibility! Sparks are flying! ✨"
    elif love_score >= 70:
        feedback = "Very compatible! This looks promising. 😊"
    elif love_score >= 60:
        feedback = "Good potential here! Worth exploring. 🤔"
    elif love_score >= 50:
        feedback = "A solid 50/50 chance! Could go either way. 🤷"
    elif love_score >= 40:
        feedback = "Hmm, some effort might be needed. 💪"
    elif love_score >= 20:
        feedback = "It's a bit of a long shot, but miracles happen! 😬"
    else: # < 20
        feedback = "Maybe... just stay friends? 😅 Or defy the odds!"
        if love_score == 0:
             feedback = "Zero? Are you sure they're not arch-nemeses? 😂 Or maybe opposites attract VERY strongly!"


    return f"💖 Calculating love compatibility for **{name1}** and **{name2}**...\n" \
           f"   Drumroll please... 🥁\n" \
           f"   Love Meter says: **{love_score}%** compatible! 💕\n" \
           f"   {feedback}"

# --- Number Guessing Command (Simple One-Shot) ---
GUESS_NUMBER_MIN = 1
GUESS_NUMBER_MAX = 10 # Small range for easier testing/playing in one shot

def guess_the_number(user_guess_str: str = None) -> str:
    """
    Plays a simple one-shot number guessing game.
    Bot picks a number, user guesses.
    """
    if not user_guess_str or not user_guess_str.strip():
        return f"🤔 Guess a number between {GUESS_NUMBER_MIN} and {GUESS_NUMBER_MAX}! Usage: /guess <number>"

    try:
        user_guess = int(user_guess_str.strip())
        if not (GUESS_NUMBER_MIN <= user_guess <= GUESS_NUMBER_MAX):
            return f"🤦 Your guess must be a number between {GUESS_NUMBER_MIN} and {GUESS_NUMBER_MAX}."
    except ValueError:
        return f"🤨 '{user_guess_str}' doesn't look like a valid number. Please guess a number."

    bot_number = random.randint(GUESS_NUMBER_MIN, GUESS_NUMBER_MAX)

    if user_guess == bot_number:
        return f"🎉 Woohoo! You guessed it! I was thinking of **{bot_number}**. You're a mind reader! 🤯"
    else:
        # Give a hint for a slightly better experience even in one-shot
        hint = ""
        if user_guess < bot_number:
            hint = "A little higher next time! 😉"
        else:
            hint = "A little lower next time! 😉"
        return f"🙁 Aw, shucks! I was thinking of **{bot_number}**. {hint} Try again with /guess!"


if __name__ == '__main__':
    print("--- Testing Fun Commands ---\n")

    print("Testing Coinflip:")
    for _ in range(5):
        print(f"  {coin_flip()}")
    print("-" * 20 + "\n")

    print("Testing Magic 8-Ball:")
    print(f"  No question: {magic_8_ball()}")
    print(f"  Question 1: {magic_8_ball('Will it rain today?')}")
    print(f"  Question 2: {magic_8_ball('Is this bot awesome?')}")
    print(f"  Question 3: {magic_8_ball('  Will I learn Python?  ')}") # Test stripping
    print("-" * 20 + "\n")

    print("Testing Rate Command:")
    print(f"  No item: {rate_something()}")
    print(f"  Item 'my cooking': {rate_something('my cooking')}")
    print(f"  Item 'this bot': {rate_something('this bot')}")
    print(f"  Item '  the weather today  ': {rate_something('  the weather today  ')}")
    print("-" * 20 + "\n")

    print("Testing RPS Command:")
    print(f"  No choice: {play_rps()}")
    print(f"  Invalid choice: {play_rps('lizard')}")
    print(f"  User picks Rock: {play_rps('rock')}")
    print(f"  User picks Paper: {play_rps('PAPER')}") # Test case insensitivity
    print(f"  User picks Scissors: {play_rps('  scissors  ')}") # Test stripping
    print("-" * 20 + "\n")

    print("Testing Truth Command:")
    for _ in range(3):
        print(f"  {get_truth_question()}")
    print("-" * 20 + "\n")

    print("Testing Dare Command:")
    for _ in range(3):
        print(f"  {get_dare_challenge()}")
    print("-" * 20 + "\n")

    print("Testing Ship Command:")
    # Mock get_env_variable for standalone testing if BOT_NAME is used
    # ... (ship test code remains the same)
    print(f"  No names: {calculate_ship_percentage('')}")
    print(f"  One name (Alice): {calculate_ship_percentage('Alice')}")
    print(f"  Two names (Alice, Bob): {calculate_ship_percentage('Alice', 'Bob')}")
    print(f"  Two names (Bob, Alice): {calculate_ship_percentage('Bob', 'Alice')}") # Should be same as above
    print(f"  Two same names (Eve, Eve): {calculate_ship_percentage('Eve', 'Eve')}")
    print(f"  Long names (Bartholomew, Gwendolyn): {calculate_ship_percentage('Bartholomew', 'Gwendolyn')}")
    print(f"  One name (TestBotShip - assuming this is bot name): {calculate_ship_percentage('TestBotShip')}")
    print("-" * 20 + "\n")

    print("Testing Guess Command:")
    print(f"  No guess: {guess_the_number()}")
    print(f"  Invalid guess (text): {guess_the_number('five')}")
    print(f"  Invalid guess (out of range low): {guess_the_number(str(GUESS_NUMBER_MIN - 1))}")
    print(f"  Invalid guess (out of range high): {guess_the_number(str(GUESS_NUMBER_MAX + 1))}")
    # Test a few valid guesses - outcome will be random
    for i in range(GUESS_NUMBER_MAX + 2): # Try to guess all numbers in a small range
        guess_val = random.randint(GUESS_NUMBER_MIN, GUESS_NUMBER_MAX)
        print(f"  Guessing {guess_val}: {guess_the_number(str(guess_val))}")
    print("-" * 20 + "\n")
