import discord
import asyncio
from discord.ext import commands
from config import TOKEN
from database import init_db


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)

COGS = [
    "cogs.moderation",
    "cogs.welcome",
    "cogs.leveling",
    "cogs.ai",
]

async def setup_hook():
    for cog in COGS:
        await bot.load_extension(cog)
    await init_db()
    await bot.tree.sync()

bot.setup_hook = setup_hook

async def main():
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())