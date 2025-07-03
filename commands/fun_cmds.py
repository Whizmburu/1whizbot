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
