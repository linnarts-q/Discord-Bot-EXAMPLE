# 🤖 Discord Multi-Feature Bot 🤖

An example of Discord bot built with **discord.py**, **SQLite** and **OpenRouter AI (Gemma)**. Built as a portfolio project demonstrating bot development, database integration and AI API usage.

---

## ✨ Features

- **Moderation** — Ban, kick and warn members. Auto-ban triggers on 3rd warning. Clear warnings with `*resurrect`
- **Welcome System** — Greets new members and assigns a default role automatically
- **Leveling & XP** — Members earn XP for activity and unlock roles at milestones
- **Jarvis AI** — Talk to the bot by mentioning its name or replying to its messages. Powered by Google Gemma via OpenRouter with per-user conversation memory

---

## 🗂️ Project Structure

```
discord-bot/
├── bot.py              # Entry point
├── config.py           # Settings and constants
├── database.py         # SQLite setup and initialization
├── cogs/
│   ├── moderation.py   # Ban, kick, warn, resurrect commands
│   ├── welcome.py      # Member join event
│   ├── leveling.py     # XP and level-up system
│   └── ai.py           # Jarvis AI listener
├── .env                # Secret keys (not committed)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Create `.env` file

```
TOKEN=your_discord_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 4. Get your API keys

**Discord Bot Token:**
1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a new application → Bot → Reset Token
3. Enable **Server Members Intent** and **Message Content Intent**
4. Invite the bot via OAuth2 → URL Generator (scopes: `bot`, `applications.commands`)

**OpenRouter API Key:**
1. Register at [openrouter.ai](https://openrouter.ai)
2. Go to Keys → Create Key (free tier available)

### 5. Run the bot

```
python bot.py
```

---

## 🎮 Commands

### Moderation
> Requires **Administrator** permission

| Command | Description | Example |
|--------|-------------|---------|
| `*ban @user [reason]` | Ban a member | `*ban @John spam` |
| `*kick @user [reason]` | Kick a member | `*kick @John` |
| `*warn @user [reason]` | Warn a member. Auto-bans on 3rd warning | `*warn @John bad behavior` |
| `*resurrect @user` | Clear all warnings and unban a member | `*resurrect @John` |

### Jarvis AI

Jarvis has two interaction modes:

| Mode | How to use | Example |
|------|-----------|---------|
| **Name trigger** | Start message with `Jarvis,` | `Jarvis, tell me a joke` |
| **Reply trigger** | Reply to any Jarvis message | Just hit reply and type |

Jarvis remembers conversation history per user.

### Leveling
Leveling is automatic — members earn XP by sending messages. Roles are assigned at these milestones:

| Level | Role          |
|-------|---------------|
| 1 | 🐣 Noob       |
| 5 | 💬 Chatterbox |
| 10 | ⚡ Regular     |
| 20 | 🔥 Veteran    |
| 50 | 👑 Legend     |

> **WARNING**: Roles must be created manually on your server with the exact same names.

---

## 🛠️ Tech Stack

- [discord.py](https://discordpy.readthedocs.io/) — Discord API wrapper
- [aiosqlite](https://aiosqlite.omnilib.dev/) — Async SQLite database
- [aiohttp](https://docs.aiohttp.org/) — Async HTTP client for AI API calls
- [OpenRouter](https://openrouter.ai/) — AI API gateway (Gemma model)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management

---