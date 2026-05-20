import discord
from discord.ext import commands
import aiohttp
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
is_ready = False

@bot.event
async def on_ready():
    global is_ready
    if not is_ready:
        print(f"✅ Ingelogd als {bot.user.name}")
        channel = await bot.fetch_channel(1504402347881926678)
        try:
            rjoke = random.randint(1, 2)
            async with aiohttp.ClientSession() as session:
                if rjoke == 1:
                    url = "https://v2.jokeapi.dev/joke/Any?"
                else:
                    url = "https://official-joke-api.appspot.com/random_joke"

                async with session.get(url) as response:
                    if response.status != 200:
                        print("❌ De grap-server gaf geen antwoord. Probeer het straks nog eens!")
                        return

                    data = await response.json()

            if "joke" in data:
                embed = discord.Embed(
                    title="JOKE TIME",
                    description=f"**{data['joke']}**",
                    color=discord.Color.brand_green()
                )
            elif "setup" in data and "delivery" in data:
                embed = discord.Embed(
                    title="JOKE TIME",
                    description=f"**{data['setup']}**\n\n*... {data['delivery']}*",
                    color=discord.Color.gold()
                )
            elif "setup" in data and "punchline" in data:
                embed = discord.Embed(
                    title="JOKE TIME",
                    description=f"**{data['setup']}**\n\n*... {data['punchline']}*",
                    color=discord.Color.gold()
                )
            else:
                print("❌ De grap is niet in het juiste formaat ontvangen.")
                return

            await channel.send(embed=embed)
        except Exception as e:
            print(f"Fout bij ophalen grap: {e}")
        is_ready = True
        await bot.close()
        

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
