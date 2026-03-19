import discord
from discord.ext import commands
from database import DB_PATH
import aiosqlite

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member} has been banned. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member} has been kicked. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT OR IGNORE INTO warnings (user_id, guild_id, reason) VALUES (?, ?, ?)",
                (member.id, ctx.guild.id, reason)
            )
            await db.commit()
        await ctx.send(f"⚠️ {member} has been warned. Reason: {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))