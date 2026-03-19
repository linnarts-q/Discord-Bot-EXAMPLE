import discord
from discord import app_commands
from discord.ext import commands
from config import AI_PROMPT, BOT_NICKNAME
import aiohttp
import os

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask AI a question")
    async def ask(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "google/gemma-3-12b-it:free",
                        "messages": [
                            {"role": "user", "content": f"{AI_PROMPT}\n\nUser question: {question}"}
                        ]
                        }
                ) as resp:
                    data = await resp.json()
                    answer = data["choices"][0]["message"]["content"]
                    if len(answer) > 1900:
                        answer = answer[:1900] + "..."
            await interaction.followup.send(
                f"**{interaction.user.display_name}:** {question}\n\n**{BOT_NICKNAME}:** {answer}"
            )
        except Exception as e:
            await interaction.followup.send(f"❌❌❌ {e} ❌❌❌")

async def setup(bot):
    await bot.add_cog(AI(bot))