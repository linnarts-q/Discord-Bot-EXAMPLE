#  Example Discord Multi-Feature Bot

A feature-rich Discord bot built with **discord.py**, **SQLite** and **OpenRouter AI (Gemma)**. Built as a example project demonstrating bot development, database integration and AI API usage.

---

##  Features

- 🛡 **Moderation** — Ban, kick, and warn members with logged reasons
-  **Welcome System** — Greets new members and assigns a default role automatically
-  **Leveling & XP** — Members earn XP for activity and unlock roles at milestones
-  **AI Command** — Ask the bot anything, powered by Google Gemma via OpenRouter

---

##  Project Structure

```
discord-bot/
├── bot.py              # Entry point
├── config.py           # Settings and constants
├── database.py         # SQLite setup and initialization
├── cogs/
│   ├── moderation.py   # Ban, kick, warn commands
│   ├── welcome.py      # Member join event
│   ├── leveling.py     # XP and level-up system
│   └── ai.py           # /ask slash command
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
2. Go to Keys → Create Key

### 5. Run the bot

```
bot.py
```

---

## 🎮 Commands

### Moderation
> Requires **Administrator** permission

| Command | Description             | Example |
|--------|-------------------------|---------|
| `*ban @user [reason]` | Ban user                | `*ban @John spam` |
| `*kick @user [reason]` | Kick user               | `*kick @John` |
| `*warn @user [reason]` | Warn user (saved to DB) | `*warn @John bad behavior` |

### AI
| Command | Description |
|--------|-------------|
| `/ask [question]` | Ask the AI anything |

### Leveling
Leveling is automatic — members earn XP by sending messages. Roles are assigned at these milestones:

| Level | Role          |
|-------|---------------|
| 1 | 🐣 Newbie     |
| 5 | 💬 Chatterbox |
| 10 | ⚡ Regular     |
| 20 | 🔥 Veteran    |
| 50 | 👑 Legend     |

---

## 🛠️ Tech Stack

- [discord.py](https://discordpy.readthedocs.io/) — Discord API wrapper
- [aiosqlite](https://aiosqlite.omnilib.dev/) — Async SQLite database
- [aiohttp](https://docs.aiohttp.org/) — Async HTTP client for AI API calls
- [OpenRouter](https://openrouter.ai/) — AI API gateway (Gemma model)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management

---