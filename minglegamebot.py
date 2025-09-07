import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler

BOT_TOKEN = "YOURTOKEN"  # Replace with your actual bot token
MIN_PLAYERS = 2
MAX_PLAYERS_PER_SESSION = 5
MAX_CONCURRENT_SESSIONS = 3

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

game_sessions = {}  # Active game sessions {session_id: session_data}
player_sessions = {}  # Tracks which session a player belongs to {player_id: session_id}

async def create_game_session():
    """Creates a new game session if the session limit is not exceeded."""
    if len(game_sessions) >= MAX_CONCURRENT_SESSIONS:
        return None  # Do not create a new session if the limit is reached

    session_id = str(random.randint(1000, 9999))
    game_sessions[session_id] = {
        "players": {},
        "target_number": random.randint(1, 8),
        "active": False,
    }
    return session_id

async def send_initial_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the main menu keyboard with a welcome message."""
    keyboard = [
        [InlineKeyboardButton("Join Game", callback_data="join")],
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Leave Game", callback_data="leave")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        "🎉 Welcome to the Mingle Number Guessing Game! 🎮\n\n"
        "Invite your friends and join the game. We need at least 2 players to start! 🤝\n"
        "Press 'Join Game' to participate or 'Help' for rules. 📚"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles players joining a game session, ensuring they are only in one session."""
    user = update.effective_user

    # Check if user is already in a session
    if user.id in player_sessions:
        await context.bot.send_message(user.id, "⚠️ You are already in a game session!")
        return

    # Find an available session
    available_sessions = [sid for sid, session in game_sessions.items() if not session["active"]]

    if available_sessions:
        session_id = available_sessions[0]
    else:
        session_id = await create_game_session()

        if not session_id:  # Max sessions reached
            await context.bot.send_message(user.id, "⚠️ Maximum game sessions reached. Try again later.")
            return

    session = game_sessions[session_id]
    session["players"][user.id] = user.first_name
    player_sessions[user.id] = session_id  # Track player's session

    await context.bot.send_message(user.id, f"✅ You have joined game session {session_id}.")

    # Start the game if enough players join
    if len(session["players"]) >= MIN_PLAYERS:
        session["active"] = True
        await notify_all_players_new_session(context, session_id)
        await send_guess_keyboard_to_all(context, session_id)

async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles players leaving their game session."""
    user = update.effective_user
    session_id = player_sessions.get(user.id)

    if not session_id or session_id not in game_sessions:
        await update.effective_message.reply_text("⚠️ You are not in any game session.")
        return

    session = game_sessions[session_id]
    del session["players"][user.id]
    del player_sessions[user.id]  # Remove from tracking

    await context.bot.send_message(user.id, "🚪 You have left the game.")

    # Remove session if empty
    if not session["players"]:
        del game_sessions[session_id]

async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles a player's guess, giving hints and checking correctness."""
    query = update.callback_query
    user = query.from_user
    user_guess = int(query.data.split("_")[1])

    session_id = player_sessions.get(user.id)

    if not session_id or session_id not in game_sessions:
        await query.answer("⚠️ You are not in an active game!")
        return

    session = game_sessions[session_id]

    if not session["active"]:
        await query.answer("⚠️ The game is not active!")
        return

    target_number = session["target_number"]

    if user_guess == target_number:
        session["active"] = False
        winner = session["players"][user.id]

        await context.bot.send_message(user.id, f"🎉 {winner}, you won! The number was {target_number}.")
        
        # End the session
        for player_id in session["players"]:
            del player_sessions[player_id]  # Remove from tracking
        del game_sessions[session_id]

    else:
        hint = "⬆️ Go higher!" if user_guess < target_number else "⬇️ Go lower!"
        await query.answer(f"❌ Wrong guess! {hint}")

async def notify_all_players_new_session(context: ContextTypes.DEFAULT_TYPE, session_id: str):
    """Notifies all players in a session that the game has started."""
    session = game_sessions[session_id]
    for player_id in session["players"]:
        await context.bot.send_message(player_id, "🎯 The game has started! Guess a number between 1 and 10.")

async def send_guess_keyboard_to_all(context: ContextTypes.DEFAULT_TYPE, session_id: str):
    """Sends the number selection keyboard to all players in a session."""
    keyboard = [[InlineKeyboardButton(str(i), callback_data=f"guess_{i}") for i in range(1, 11)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    session = game_sessions[session_id]

    for player_id in session["players"]:
        await context.bot.send_message(player_id, "🔢 Make a guess:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all button interactions."""
    query = update.callback_query
    data = query.data

    if data == "join":
        await join(update, context)
    elif data == "help":
        await query.answer("ℹ️ This is a number guessing game. Join a game and guess a number between 1 and 10. The first correct guess wins!")
    elif data == "leave":
        await leave(update, context)
    elif data.startswith("guess_"):
        await handle_guess(update, context)

def main():
    """Starts the bot."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", send_initial_keyboard))
    app.add_handler(CallbackQueryHandler(button_handler))

    logging.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
