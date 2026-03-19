import discord
from discord.ext import commands
from database import DB_PATH
import aiosqlite
import random

LEVEL_ROLES = {
    1:  "🐣 Newbie",
    5:  "💬 Chatterbox",
    10: "⚡ Regular",
    20: "🔥 Veteran",
    50: "👑 Legend",
}

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        xp_gain = random.randint(5, 20)

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT INTO levels (user_id, guild_id, xp, level)
                VALUES (?, ?, ?, 0)
                ON CONFLICT(user_id, guild_id)
                DO UPDATE SET xp = xp + ?
            """, (message.author.id, message.guild.id, xp_gain, xp_gain))
            await db.commit()

            cursor = await db.execute(
                "SELECT xp, level FROM levels WHERE user_id=? AND guild_id=?",
                (message.author.id, message.guild.id),
            )
            row = await cursor.fetchone()
            xp, level = row

        xp_needed = 100 * level
        if xp >= xp_needed and level > 0:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE levels SET level = level + 1, xp = 0 WHERE user_id=? AND guild_id=?",
                    (message.author.id, message.guild.id)
                )
                await db.commit()
            await message.channel.send(
                f"🎉 {message.author.mention} leveled up to level **{level + 1}**!"
            )
            await self.assign_role(message, level + 1)

    async def assign_role(self, message, level):
        if level in LEVEL_ROLES:
            role_name = LEVEL_ROLES[level]
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role:
                await message.author.add_roles(role)

async def setup(bot):
    await bot.add_cog(Leveling(bot))