import discord
import aiosqlite
from discord.ext import commands
from database import DB_PATH

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.message.delete()
        await member.ban(reason=reason)
        await ctx.send(f"⚠️ {member} has been banned. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.message.delete()
        await member.kick(reason=reason)
        await ctx.send(f"⚠️ {member} has been kicked. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.message.delete()
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM warnings WHERE user_id=? AND guild_id=?",
                (member.id, ctx.guild.id)
            )
            row = await cursor.fetchone()
            warn_count = row[0]
            if warn_count >= 3:
                await member.ban(reason="Warning limit reached")
                await ctx.send(f"⚠️ {member} has reached 3 warnings and has been auto-banned.")
                return
            else:
                await db.execute(
                    "INSERT OR IGNORE INTO warnings (user_id, guild_id, reason) VALUES (?, ?, ?)",
                    (member.id, ctx.guild.id, reason)
                )
                await db.commit()
                await ctx.send(f"⚠️ {member} has been warned. Warn: {warn_count + 1}/3. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resurrect(self, ctx, member: discord.Member):
        await ctx.message.delete()
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "DELETE FROM warnings WHERE user_id=? AND guild_id=?",
                (member.id, ctx.guild.id)
            )
            await db.commit()
        try:
            await ctx.guild.unban(member)
        except discord.NotFound:
            pass
        await ctx.send(f"✅ {member} has been resurrected.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))