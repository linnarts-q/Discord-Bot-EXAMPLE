import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(
                f"👋 Welcome to **{member.guild.name}**, {member.mention}!\n"
            )

        role = discord.utils.get(member.guild.roles, name="Rookie")
        if role:
            await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(Welcome(bot))