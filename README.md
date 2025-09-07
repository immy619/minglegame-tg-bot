# 🎮 Mingle Game Bot

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/telegram-bot-blue.svg)](https://telegram.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A fun **multiplayer number guessing game** for Telegram! Players join a session, guess a number between 1 and 10, and race to be the first to find the correct number.  

---

## 🚀 Features

- Multiple concurrent game sessions (default: 3).  
- Each session supports **2–5 players**.  
- Interactive **inline keyboards** for joining, leaving, and guessing.  
- Hints for wrong guesses (⬆️ higher / ⬇️ lower).  
- Automatic session cleanup when all players leave or a winner is declared.  
- Lightweight Python bot using `python-telegram-bot`.  

---

## 🎮 How to Play

1. Start the bot with `/start`.  
2. Press **Join Game** to enter a session.  
3. Wait for at least 2 players to start the game.  
4. Guess a number between 1 and 10 using the inline buttons.  
5. The first correct guess wins! 🎉  
6. Press **Leave Game** anytime to exit the session.  

**Inline Buttons:**

- **Join Game** → Enter a game session.  
- **Leave Game** → Exit your current session.  
- **Help** → Show game instructions.  
- **Number buttons (1–10)** → Make a guess during an active game.  

---

## 💻 Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/mingle-game-bot.git
cd mingle-game-bot
pip install python-telegram-bot --upgrade
BOT_TOKEN = "YOURTOKEN"
python bot.py

⚙️ Configuration

You can adjust these constants in bot.py:

| Variable                  | Description                                      |
| ------------------------- | ------------------------------------------------ |
| `BOT_TOKEN`               | Your Telegram bot token from BotFather.          |
| `MIN_PLAYERS`             | Minimum players to start a session (default: 2). |
| `MAX_PLAYERS_PER_SESSION` | Maximum players per session (default: 5).        |
| `MAX_CONCURRENT_SESSIONS` | Maximum concurrent sessions (default: 3).        |

🔧 How It Works

Players join using Join Game.

Once enough players join, the session becomes active.

Players guess numbers via inline buttons.

Bot provides hints for incorrect guesses.

First correct guess ends the session and declares the winner.

If all players leave, the session is automatically deleted
