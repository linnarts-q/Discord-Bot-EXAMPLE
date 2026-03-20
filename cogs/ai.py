import aiosqlite
import asyncio
import aiohttp
import os
from discord.ext import commands
from config import AI_PROMPT, BOT_NAME
from database import DB_PATH

HISTORY_LIMIT = 3

async def get_history(user_id, guild_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT role, content FROM conversations "
            "WHERE user_id=? AND guild_id=? "
            "ORDER BY timestamp DESC LIMIT ?",
            (user_id, guild_id, HISTORY_LIMIT)
        )
        rows = await cursor.fetchall()
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

async def save_message(user_id, guild_id, role, content):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO conversations (user_id, guild_id, role, content) VALUES (?, ?, ?, ?)",
            (user_id, guild_id, role, content)
        )
        await db.commit()

async def ask_ai(messages):
    for attempt in range(50):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "google/gemma-3-12b-it:free",
                    "messages": messages
                }
            ) as resp:
                data = await resp.json()
                print(data)
                if "error" in data and data["error"].get("code") == 429:
                    await asyncio.sleep(5)
                    continue
                return data["choices"][0]["message"]["content"]
    return "⚠️ Something went wrong, try again later. ⚠️"

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        print(f"MSG: '{message.content}' | starts: {message.content.lower().startswith(f'{BOT_NAME.lower()},')}")

        question = None
        use_history = False

        if message.content.lower().startswith(f"{BOT_NAME.lower()},"):
            question = message.content[len(BOT_NAME) + 1:].strip()
            use_history = True

        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            if ref_msg.author.id == self.bot.user.id:
                question = message.content
                use_history = True

        if not question:
            return

        async with message.channel.typing():
            try:
                if use_history:
                    history = await get_history(message.author.id, message.guild.id)
                    history.append({"role": "user", "content": f"{AI_PROMPT}\n\n{question}"})
                    messages = history
                else:
                    messages = [{"role": "user", "content":
                        f"{AI_PROMPT}\n\nContext: {ref_msg.content}\n\nQuestion: {question}"}]

                answer = await ask_ai(messages)
                if len(answer) > 1900:
                    answer = answer[:1900] + "..."

                await save_message(message.author.id, message.guild.id, "user", question)
                await save_message(message.author.id, message.guild.id, "assistant", answer)

                await message.reply(f"{answer}")

            except Exception as e:
                await message.reply(f"❌ Something went wrong. Error: {e}")

async def setup(bot):
    await bot.add_cog(AI(bot))